"""Station Graph: central intermediate representation for the solver.

A solution is a dataflow graph where atoms flow through stations:
    Input Station -> Glyph Station(s) -> Bonder Station -> Output Station

Each atom traces a path (a Flow) through this graph. The graph captures
ALL constraints in one place:
  - Chemical: what atom type enters/exits each station
  - Spatial: bonder slots must align with output bond directions
  - Ordering: which stations must be visited before which
  - Resource: how many arm directions are needed (max 6)

Construction: build_station_graph(puzzle, analysis) -> List[StationGraph]
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set

from .puzzle import AtomType, Puzzle
from .hex import HexCoord, DIRECTIONS
from .recipe import PuzzleAnalysis, Reaction, REACTION_GLYPHS
from .glyph_model import (GlyphSpec, GLYPH_SPECS, get_glyph_spec,
                           local_to_world, footprint_world)


# ---------------------------------------------------------------------------
# Core data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class StationID:
    """Unique identifier for a station in the graph."""
    kind: str      # 'input', 'glyph', 'bonder', 'unbonder', 'output'
    index: int     # disambiguator within kind

    def __repr__(self) -> str:
        return f"{self.kind}:{self.index}"


@dataclass
class Station:
    """A station in the dataflow graph."""
    id: StationID
    part_name: str           # omsim part name (e.g. 'glyph-calcification', 'bonder-speed')
    io_index: int = 0        # for input/output: puzzle io index
    arm_direction: int = -1  # 0-5, filled during layout
    position: Optional[HexCoord] = None
    rotation: int = 0


@dataclass
class Flow:
    """One atom's journey through the graph."""
    flow_id: int
    source: StationID        # where to grab
    dest: StationID          # where to deliver (bonder or output)
    via: List[StationID]     # intermediate glyph stations (pass-through)
    atom_type_in: AtomType   # type when grabbed from source
    atom_type_out: AtomType  # type when delivered to dest
    needs_ungrab: bool       # conversion glyph: must drop before glyph fires
    priority: int            # assembly order (0 = first)


@dataclass
class SlotConstraint:
    """A spatial constraint between two stations."""
    station_a: StationID
    station_b: StationID
    constraint_type: str     # 'aligned', 'adjacent', 'ordered'
    bond_direction: Optional[Tuple[int, int]] = None  # (dq, dr) for bonder-output


@dataclass
class StationGraph:
    """The central IR: stations, flows, and constraints."""
    stations: Dict[StationID, Station]
    flows: List[Flow]
    constraints: List[SlotConstraint]
    assembly_order: List[int]  # flow_ids in delivery order
    # Metadata from planning
    glyph_names: List[str] = field(default_factory=list)
    need_bonder: bool = False
    need_unbonder: bool = False
    bonder_type: str = 'bonder'
    estimated_cost: int = 0


# ---------------------------------------------------------------------------
# Phase 1: Create stations
# ---------------------------------------------------------------------------

def _create_input_stations(puzzle: Puzzle) -> Dict[StationID, Station]:
    """Create input stations from puzzle inputs."""
    stations = {}
    for i, pio in enumerate(puzzle.inputs):
        sid = StationID('input', i)
        stations[sid] = Station(
            id=sid,
            part_name='input',
            io_index=pio.index,
        )
    return stations


def _create_glyph_stations(glyph_names: List[str]) -> Dict[StationID, Station]:
    """Create glyph stations from required glyph list."""
    stations = {}
    for i, gname in enumerate(glyph_names):
        sid = StationID('glyph', i)
        stations[sid] = Station(
            id=sid,
            part_name=gname,
        )
    return stations


def _create_bonder_station(bonder_type: str) -> Tuple[StationID, Station]:
    """Create a bonder station."""
    sid = StationID('bonder', 0)
    return sid, Station(id=sid, part_name=bonder_type)


def _create_output_station() -> Tuple[StationID, Station]:
    """Create the output station."""
    sid = StationID('output', 0)
    return sid, Station(id=sid, part_name='out-std', io_index=0)


# ---------------------------------------------------------------------------
# Phase 2: Create flows
# ---------------------------------------------------------------------------

def _trace_flows(puzzle: Puzzle, analysis: PuzzleAnalysis,
                 stations: Dict[StationID, Station],
                 reactions: Dict[Reaction, int]) -> List[Flow]:
    """Trace each output atom backwards to create flows."""
    if not puzzle.outputs:
        return []

    output_mol = puzzle.outputs[0].molecule
    flows: List[Flow] = []

    # Build input element -> StationID mapping
    input_elem_to_sid: Dict[AtomType, List[StationID]] = {}
    for sid, station in stations.items():
        if sid.kind == 'input':
            pio = puzzle.inputs[station.io_index] if station.io_index < len(puzzle.inputs) else None
            if pio and pio.molecule.is_monoatomic:
                elem = pio.molecule.atoms[0].atom_type
                input_elem_to_sid.setdefault(elem, []).append(sid)

    # Build glyph name -> StationID mapping
    glyph_name_to_sid: Dict[str, List[StationID]] = {}
    for sid, station in stations.items():
        if sid.kind == 'glyph':
            glyph_name_to_sid.setdefault(station.part_name, []).append(sid)

    # Find bonder and output stations
    bonder_sid = None
    output_sid = None
    for sid in stations:
        if sid.kind == 'bonder':
            bonder_sid = sid
        elif sid.kind == 'output':
            output_sid = sid

    if output_sid is None:
        return []

    # Compute assembly order
    assembly_order = _compute_assembly_order(output_mol)

    # Track grab counts per input
    grab_counts: Dict[StationID, int] = {}

    for priority, atom_idx in enumerate(assembly_order):
        if atom_idx >= len(output_mol.atoms):
            continue
        atom = output_mol.atoms[atom_idx]
        out_type = atom.atom_type

        # Trace backwards to find source type and glyph visits
        source_type, glyph_visits, needs_ungrab = _trace_single_atom(
            out_type, reactions, analysis)

        # Find input station
        source_sid = _find_input_sid(source_type, input_elem_to_sid, puzzle, stations)
        if source_sid is None:
            continue

        # Find glyph stations for via path
        via_sids: List[StationID] = []
        for gname in glyph_visits:
            if gname in glyph_name_to_sid:
                sids = glyph_name_to_sid[gname]
                # Use round-robin for multi-instance glyphs
                idx = grab_counts.get(source_sid, 0) % len(sids)
                via_sids.append(sids[min(idx, len(sids) - 1)])

        # Determine destination: bonder if bonding needed, else output
        if analysis.needs_bonding and bonder_sid is not None:
            dest_sid = bonder_sid
        else:
            dest_sid = output_sid

        flows.append(Flow(
            flow_id=len(flows),
            source=source_sid,
            dest=dest_sid,
            via=via_sids,
            atom_type_in=source_type,
            atom_type_out=out_type,
            needs_ungrab=needs_ungrab,
            priority=priority,
        ))

        grab_counts[source_sid] = grab_counts.get(source_sid, 0) + 1

    # Add bonder->output flow if bonding is needed
    # This represents picking up the bonded molecule and delivering to output
    if analysis.needs_bonding and bonder_sid is not None and output_sid is not None:
        # The bonded molecule flow: grab from bonder, deliver to output
        # Use the output molecule's first atom type as representative
        out_type = output_mol.atoms[0].atom_type if output_mol.atoms else AtomType.SALT
        flows.append(Flow(
            flow_id=len(flows),
            source=bonder_sid,
            dest=output_sid,
            via=[],
            atom_type_in=out_type,
            atom_type_out=out_type,
            needs_ungrab=False,
            priority=len(assembly_order),  # last in assembly order
        ))

    return flows


def _trace_single_atom(out_type: AtomType,
                        reactions: Dict[Reaction, int],
                        analysis: PuzzleAnalysis
                        ) -> Tuple[AtomType, List[str], bool]:
    """Trace one output atom backwards to find source type and glyph visits.

    Handles multi-step reaction chains. For example, if output needs Gold
    but inputs only have Lead:
      - source = Lead, via = ['glyph-purification', 'glyph-projection']
    If Quicksilver is needed for projection but not in inputs and purification
    is available, the chain is extended accordingly.
    """
    from .puzzle import METAL_CHAIN

    # Salt from calcification
    if out_type == AtomType.SALT and reactions.get(Reaction.CALCIFICATION, 0) > 0:
        for elem in [AtomType.AIR, AtomType.EARTH, AtomType.FIRE, AtomType.WATER]:
            if elem in analysis.input_elements:
                return (elem, ['glyph-calcification'], False)

    # Vitae/Mors from animismus
    if out_type in (AtomType.VITAE, AtomType.MORS):
        if reactions.get(Reaction.ANIMISMUS, 0) > 0:
            return (AtomType.SALT, ['glyph-life-and-death'], True)

    # Metal from projection (with multi-step chain support)
    if out_type.is_metal and reactions.get(Reaction.PROJECTION, 0) > 0:
        # Quicksilver is the default source for projection
        source = AtomType.QUICKSILVER
        via = ['glyph-projection']

        # Check if Quicksilver is directly available in inputs
        if AtomType.QUICKSILVER not in analysis.input_elements:
            # Quicksilver not in inputs -- check if purification can produce it
            if reactions.get(Reaction.PURIFICATION, 0) > 0:
                # Find the highest-rank metal available in inputs to purify
                purify_source = _find_purification_source(analysis)
                if purify_source is not None:
                    source = purify_source
                    via = ['glyph-purification', 'glyph-projection']

        return (source, via, False)

    # Quicksilver needed but not in inputs -- resolve via purification
    if out_type == AtomType.QUICKSILVER:
        if reactions.get(Reaction.PURIFICATION, 0) > 0:
            purify_source = _find_purification_source(analysis)
            if purify_source is not None:
                return (purify_source, ['glyph-purification'], False)
        if out_type in analysis.input_elements:
            return (out_type, [], False)

    # Cardinal from Van Berlo
    if out_type.is_cardinal and reactions.get(Reaction.VAN_BERLO, 0) > 0:
        if out_type not in analysis.input_elements:
            return (AtomType.SALT, ['glyph-duplication'], False)

    # Direct: same type available in input
    if out_type in analysis.input_elements:
        return (out_type, [], False)

    # Metal not in inputs -- try purification chain (higher metal -> lower metal)
    if out_type.is_metal and reactions.get(Reaction.PURIFICATION, 0) > 0:
        # Find a higher metal in inputs that can be purified down
        target_rank = out_type.metal_rank
        for metal in reversed(METAL_CHAIN):
            if metal.metal_rank > target_rank and metal in analysis.input_elements:
                steps = metal.metal_rank - target_rank
                via = ['glyph-purification'] * steps
                return (metal, via, False)

    return (out_type, [], False)


def _find_purification_source(analysis: PuzzleAnalysis) -> Optional[AtomType]:
    """Find the best metal in inputs to purify for Quicksilver production.

    Returns the highest-rank metal available in inputs (above Lead, since
    purifying Lead produces nothing below it). Purification of metal[i]
    yields metal[i-1] + Quicksilver.
    """
    from .puzzle import METAL_CHAIN

    # Search from highest metal down; any metal above Lead can be purified
    for metal in reversed(METAL_CHAIN):
        if metal == METAL_CHAIN[0]:
            continue  # Can't purify the lowest metal usefully
        if metal in analysis.input_elements:
            return metal
    # Fallback: even Lead could be purified in some game contexts
    if METAL_CHAIN[0] in analysis.input_elements:
        return METAL_CHAIN[0]
    return None


def _find_input_sid(atom_type: AtomType,
                     input_elem_to_sid: Dict[AtomType, List[StationID]],
                     puzzle: Puzzle,
                     stations: Dict[StationID, Station]) -> Optional[StationID]:
    """Find input station that provides the given atom type."""
    if atom_type in input_elem_to_sid:
        return input_elem_to_sid[atom_type][0]

    # Search all input stations
    for sid, station in stations.items():
        if sid.kind == 'input':
            pio_idx = station.io_index
            if pio_idx < len(puzzle.inputs):
                pio = puzzle.inputs[pio_idx]
                for atom in pio.molecule.atoms:
                    if atom.atom_type == atom_type:
                        return sid

    return None


def _compute_assembly_order(molecule) -> List[int]:
    """BFS from each leaf atom; return the ordering with minimal total index spread.

    For each leaf as BFS root, score = sum of |order[i+1] - order[i]| over
    consecutive pairs. Lower score means more spatially compact delivery order.
    """
    atoms = molecule.atoms
    bonds = molecule.bonds
    n = len(atoms)

    if n <= 1:
        return list(range(n))

    pos_to_idx = {atom.position: i for i, atom in enumerate(atoms)}
    adj: Dict[int, List[int]] = {i: [] for i in range(n)}

    for bond in bonds:
        fi = pos_to_idx.get(bond.from_pos)
        ti = pos_to_idx.get(bond.to_pos)
        if fi is not None and ti is not None:
            adj[fi].append(ti)
            adj[ti].append(fi)

    leaves = [i for i in range(n) if len(adj[i]) <= 1]
    if not leaves:
        leaves = [0]

    def _bfs_from(start: int) -> List[int]:
        visited: Set[int] = set()
        order: List[int] = []
        queue = [start]
        visited.add(start)
        while queue:
            node = queue.pop(0)
            order.append(node)
            for neighbor in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        # Append any disconnected nodes
        for i in range(n):
            if i not in visited:
                order.append(i)
        return order

    def _score(order: List[int]) -> int:
        return sum(abs(order[i + 1] - order[i]) for i in range(len(order) - 1))

    best_order = None
    best_score = None
    for leaf in leaves:
        candidate = _bfs_from(leaf)
        s = _score(candidate)
        if best_score is None or s < best_score:
            best_score = s
            best_order = candidate

    return best_order


# ---------------------------------------------------------------------------
# Phase 3: Derive spatial constraints
# ---------------------------------------------------------------------------

def _derive_bonder_output_constraints(
        puzzle: Puzzle,
        stations: Dict[StationID, Station]) -> List[SlotConstraint]:
    """Derive bonder-output alignment constraints from output bond directions.

    For each bond in the output molecule, emit an alignment constraint
    requiring that the bonder's slot positions physically overlap with
    the output molecule's atom positions at those bond endpoints.
    """
    constraints: List[SlotConstraint] = []

    bonder_sid = None
    output_sid = None
    for sid in stations:
        if sid.kind == 'bonder':
            bonder_sid = sid
        elif sid.kind == 'output':
            output_sid = sid

    if bonder_sid is None or output_sid is None:
        return constraints

    if not puzzle.outputs:
        return constraints

    output_mol = puzzle.outputs[0].molecule
    if not output_mol.bonds:
        return constraints

    # Collect unique bond directions in the output molecule
    bond_dirs: Set[Tuple[int, int]] = set()
    for bond in output_mol.bonds:
        dq = bond.to_pos.q - bond.from_pos.q
        dr = bond.to_pos.r - bond.from_pos.r
        bond_dirs.add((dq, dr))
        # Also add reverse direction
        bond_dirs.add((-dq, -dr))

    for dq, dr in bond_dirs:
        constraints.append(SlotConstraint(
            station_a=bonder_sid,
            station_b=output_sid,
            constraint_type='aligned',
            bond_direction=(dq, dr),
        ))

    return constraints


def valid_bonder_output_rotations(
        output_mol,
        bonder_name: str,
        output_pos: HexCoord,
        output_rot: int,
        bonder_pos: HexCoord) -> List[int]:
    """Return list of valid bonder rotations given output placement.

    Checks that every bond in the output molecule has both endpoint atoms
    positioned on bonder slot positions.
    """
    try:
        bonder_spec = get_glyph_spec(bonder_name)
    except KeyError:
        return list(range(6))

    # Compute output atom world positions
    output_atom_positions: Set[Tuple[int, int]] = set()
    for atom in output_mol.atoms:
        wp = local_to_world(output_pos, output_rot,
                            atom.position.q, atom.position.r)
        output_atom_positions.add((wp.q, wp.r))

    valid = []
    for bonder_rot in range(6):
        # Compute bonder slot world positions
        bonder_slot_positions: Set[Tuple[int, int]] = set()
        for slot in bonder_spec.active_slots:
            sp = local_to_world(bonder_pos, bonder_rot, slot.du, slot.dv)
            bonder_slot_positions.add((sp.q, sp.r))

        # Check: for every bond, both from_pos and to_pos (in world coords)
        # must be on bonder slots
        all_bonds_aligned = True
        for bond in output_mol.bonds:
            from_world = local_to_world(output_pos, output_rot,
                                         bond.from_pos.q, bond.from_pos.r)
            to_world = local_to_world(output_pos, output_rot,
                                       bond.to_pos.q, bond.to_pos.r)
            from_key = (from_world.q, from_world.r)
            to_key = (to_world.q, to_world.r)

            # At least one slot pair must contain both bond endpoints
            pair_found = (from_key in bonder_slot_positions and
                          to_key in bonder_slot_positions)
            if not pair_found:
                all_bonds_aligned = False
                break

        if all_bonds_aligned:
            valid.append(bonder_rot)

    return valid


def _count_required_directions(flows: List[Flow],
                                stations: Dict[StationID, Station]) -> int:
    """Count how many distinct arm directions would be needed."""
    # Each station needs a unique direction. Count unique stations used.
    used_sids: Set[StationID] = set()
    for flow in flows:
        used_sids.add(flow.source)
        used_sids.add(flow.dest)
        for via in flow.via:
            used_sids.add(via)
    return len(used_sids)


# ---------------------------------------------------------------------------
# Main construction
# ---------------------------------------------------------------------------

def build_station_graph(puzzle: Puzzle,
                         analysis: PuzzleAnalysis) -> List[StationGraph]:
    """Build station graph variants from puzzle analysis.

    Returns multiple graph variants:
    - Single-instance glyphs (cost-minimizing)
    - Multi-instance glyphs (cycle-minimizing)
    """
    if not puzzle.outputs:
        return []

    recipe = analysis.recipe
    reactions = recipe.reactions if recipe else {}

    graphs: List[StationGraph] = []

    # Generate glyph list variants
    glyph_variants = []
    glyphs_single = _glyph_list_single(reactions)
    glyph_variants.append(glyphs_single)
    glyphs_multi = _glyph_list_multi(reactions)
    if glyphs_multi != glyphs_single:
        glyph_variants.append(glyphs_multi)

    # Determine bonder type
    bonder_type = _determine_bonder_type(puzzle)

    for glyph_names in glyph_variants:
        # Phase 1: Create stations
        stations: Dict[StationID, Station] = {}

        # Input stations
        input_stations = _create_input_stations(puzzle)
        stations.update(input_stations)

        # Glyph stations
        glyph_stations = _create_glyph_stations(glyph_names)
        stations.update(glyph_stations)

        # Bonder station
        if analysis.needs_bonding:
            bonder_sid, bonder_station = _create_bonder_station(bonder_type)
            stations[bonder_sid] = bonder_station

        # Unbonder station
        if analysis.needs_unbonding:
            unbonder_sid = StationID('unbonder', 0)
            stations[unbonder_sid] = Station(
                id=unbonder_sid,
                part_name='unbonder',
            )

        # Output station
        output_sid, output_station = _create_output_station()
        stations[output_sid] = output_station

        # Phase 2: Create flows
        flows = _trace_flows(puzzle, analysis, stations, reactions)
        if not flows:
            continue

        # Phase 3: Derive constraints
        constraints = _derive_bonder_output_constraints(puzzle, stations)

        # Check direction count feasibility
        n_dirs = _count_required_directions(flows, stations)
        if n_dirs > 6:
            continue

        # Assembly order is just flow_ids in priority order
        assembly_order = sorted([f.flow_id for f in flows],
                                key=lambda fid: next(
                                    f.priority for f in flows if f.flow_id == fid))

        # Estimate cost
        from .solution import PART_COSTS
        cost = 20  # arm1
        for gname in glyph_names:
            cost += PART_COSTS.get(gname, 0)
        if analysis.needs_bonding:
            cost += PART_COSTS.get(bonder_type, 10)

        graph = StationGraph(
            stations=stations,
            flows=flows,
            constraints=constraints,
            assembly_order=assembly_order,
            glyph_names=glyph_names,
            need_bonder=analysis.needs_bonding,
            need_unbonder=analysis.needs_unbonding,
            bonder_type=bonder_type,
            estimated_cost=cost,
        )
        graphs.append(graph)

    # Sort by estimated cost
    graphs.sort(key=lambda g: g.estimated_cost)
    return graphs


# ---------------------------------------------------------------------------
# Helpers (absorbed from production_planner.py)
# ---------------------------------------------------------------------------

def _glyph_list_single(reactions: Dict[Reaction, int]) -> List[str]:
    """1 glyph instance per type (cost-min)."""
    glyphs = []
    for reaction, count in reactions.items():
        if count > 0:
            for glyph_name in REACTION_GLYPHS[reaction]:
                if glyph_name == 'baron':
                    continue
                glyphs.append(glyph_name)
    return glyphs


def _glyph_list_multi(reactions: Dict[Reaction, int]) -> List[str]:
    """N instances = recipe count (cycle-min)."""
    glyphs = []
    for reaction, count in reactions.items():
        if count > 0:
            for glyph_name in REACTION_GLYPHS[reaction]:
                if glyph_name == 'baron':
                    continue
                glyphs.extend([glyph_name] * count)
    return glyphs


def _determine_bonder_type(puzzle: Puzzle) -> str:
    """Determine bonder type based on output bond directions."""
    from .puzzle import PartFlag
    for pio in puzzle.outputs:
        if len(pio.molecule.bonds) <= 1:
            continue
        bond_dirs = set()
        for bond in pio.molecule.bonds:
            dq = bond.to_pos.q - bond.from_pos.q
            dr = bond.to_pos.r - bond.from_pos.r
            bond_dirs.add((dq, dr))
        if len(bond_dirs) > 1 and puzzle.has_part(PartFlag.MULTI_BONDER):
            return 'bonder-speed'
    return 'bonder'


# ---------------------------------------------------------------------------
# Graph-to-Plan adapter (backward compatibility)
# ---------------------------------------------------------------------------

def graph_to_plan(graph: StationGraph, puzzle: Puzzle,
                   analysis: PuzzleAnalysis):
    """Convert a StationGraph back to a ProductionPlan for backward compat."""
    from .production_planner import ProductionPlan, AtomRoute, InputSchedule

    routes = []
    for flow in graph.flows:
        # Find source input index
        source_station = graph.stations[flow.source]
        glyph_visits = [graph.stations[via].part_name for via in flow.via]

        routes.append(AtomRoute(
            atom_id=flow.flow_id,
            output_atom_type=flow.atom_type_out,
            source_input_idx=source_station.io_index,
            source_atom_type=flow.atom_type_in,
            grab_number=flow.priority,
            glyph_visits=glyph_visits,
            needs_ungrabbed=flow.needs_ungrab,
        ))

    # Compute input schedule
    grabs: Dict[int, int] = {}
    types: Dict[int, AtomType] = {}
    for route in routes:
        idx = route.source_input_idx
        grabs[idx] = grabs.get(idx, 0) + 1
        types[idx] = route.source_atom_type

    input_schedule = [
        InputSchedule(input_idx=idx, atom_type=types[idx],
                      grabs_per_cycle=grabs[idx])
        for idx in sorted(grabs.keys())
    ]

    return ProductionPlan(
        input_schedule=input_schedule,
        glyph_names=graph.glyph_names,
        need_bonder=graph.need_bonder,
        need_unbonder=graph.need_unbonder,
        bonder_type=graph.bonder_type,
        atom_routes=routes,
        assembly_order=graph.assembly_order,
        total_grabs=sum(s.grabs_per_cycle for s in input_schedule),
        estimated_cost=graph.estimated_cost,
    )
