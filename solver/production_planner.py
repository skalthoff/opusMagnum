"""Production planner: stoichiometry-driven precalculation of atom routes.

Analyzes what atoms need to go where before layout/tape generation,
turning the problem into pure logistics. Handles:
- Multi-glyph instancing (e.g., 2 calcification glyphs)
- Multi-grab scheduling (same input grabbed N times per output cycle)
- Assembly ordering for bonded outputs
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .puzzle import AtomType, Puzzle, METAL_CHAIN
from .hex import HexCoord
from .recipe import (PuzzleAnalysis, Reaction, Recipe,
                     REACTION_GLYPHS, REACTION_GLYPH_COST)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class AtomRoute:
    """One atom's journey from input to output position."""
    atom_id: int                     # unique per output cycle
    output_atom_type: AtomType       # what it must be at output
    source_input_idx: int            # which puzzle input (io_index)
    source_atom_type: AtomType       # what input provides
    grab_number: int                 # nth grab from this input (0-based)
    glyph_visits: List[str]          # glyph names to pass through
    needs_ungrabbed: bool            # must drop at conversion glyph


@dataclass
class InputSchedule:
    """How many times to grab from a specific input per output cycle."""
    input_idx: int
    atom_type: AtomType
    grabs_per_cycle: int


@dataclass
class ProductionPlan:
    """Complete production plan for one output cycle."""
    input_schedule: List[InputSchedule]
    glyph_names: List[str]           # WITH duplicates for multi-instance
    need_bonder: bool
    need_unbonder: bool
    bonder_type: str                 # 'bonder' or 'bonder-speed'
    atom_routes: List[AtomRoute]
    assembly_order: List[int]        # atom_ids in delivery order for bonding
    total_grabs: int                 # sum of all grabs per output cycle
    estimated_cost: int


# ---------------------------------------------------------------------------
# Planning algorithm
# ---------------------------------------------------------------------------

def generate_plans(puzzle: Puzzle, analysis: PuzzleAnalysis) -> List[ProductionPlan]:
    """Generate production plans for the puzzle.

    Returns a list of plan variants (cost-min and cycle-min) that the
    search loop can iterate over.
    """
    if not puzzle.outputs:
        return []

    output_mol = puzzle.outputs[0].molecule
    recipe = analysis.recipe
    reactions = recipe.reactions if recipe else {}

    # Step 1: Trace atom routes
    atom_routes = _trace_atom_routes(puzzle, analysis, reactions)
    if not atom_routes:
        # Fallback: if tracing fails, create a minimal plan from recipe
        return _fallback_plans(puzzle, analysis)

    # Step 2: Compute input schedule
    input_schedule = _compute_input_schedule(atom_routes, puzzle)
    total_grabs = sum(s.grabs_per_cycle for s in input_schedule)

    # Step 3: Compute assembly order
    assembly_order = _compute_assembly_order(output_mol)

    # Step 3b: Determine bonder type
    bonder_type = _determine_bonder_type(puzzle)

    # Step 4: Generate plan variants
    plans = []

    # Variant A: 1 glyph instance per type (cost-min)
    glyphs_a = _glyph_list_single(reactions)
    cost_a = _estimate_cost(glyphs_a, analysis, bonder_type)
    plans.append(ProductionPlan(
        input_schedule=input_schedule,
        glyph_names=glyphs_a,
        need_bonder=analysis.needs_bonding,
        need_unbonder=analysis.needs_unbonding,
        bonder_type=bonder_type,
        atom_routes=atom_routes,
        assembly_order=assembly_order,
        total_grabs=total_grabs,
        estimated_cost=cost_a,
    ))

    # Variant B: N glyph instances = recipe count (cycle-min)
    glyphs_b = _glyph_list_multi(reactions)
    if glyphs_b != glyphs_a:
        cost_b = _estimate_cost(glyphs_b, analysis, bonder_type)
        plans.append(ProductionPlan(
            input_schedule=input_schedule,
            glyph_names=glyphs_b,
            need_bonder=analysis.needs_bonding,
            need_unbonder=analysis.needs_unbonding,
            bonder_type=bonder_type,
            atom_routes=atom_routes,
            assembly_order=assembly_order,
            total_grabs=total_grabs,
            estimated_cost=cost_b,
        ))

    # Sort by estimated cost (cheapest first)
    plans.sort(key=lambda p: p.estimated_cost)
    return plans


# ---------------------------------------------------------------------------
# Step 1: Trace atom routes
# ---------------------------------------------------------------------------

def _trace_atom_routes(puzzle: Puzzle, analysis: PuzzleAnalysis,
                       reactions: Dict[Reaction, int]) -> List[AtomRoute]:
    """For each atom in the output, trace backwards to determine source input."""
    if not puzzle.outputs:
        return []

    output_mol = puzzle.outputs[0].molecule
    routes: List[AtomRoute] = []

    # Build input element -> io_index mapping
    input_elem_to_idx: Dict[AtomType, List[int]] = {}
    for pio in puzzle.inputs:
        if pio.molecule.is_monoatomic:
            elem = pio.molecule.atoms[0].atom_type
            input_elem_to_idx.setdefault(elem, []).append(pio.index)

    # Track grab counts per input index
    grab_counts: Dict[int, int] = {}

    for atom_id, atom in enumerate(output_mol.atoms):
        out_type = atom.atom_type
        source_type, glyph_visits, needs_ungrabbed = _trace_single_atom(
            out_type, reactions, analysis)

        # Find which input provides source_type
        source_idx = _find_input_for_type(source_type, input_elem_to_idx, puzzle)
        if source_idx is None:
            # Can't find source; skip
            continue

        grab_num = grab_counts.get(source_idx, 0)
        grab_counts[source_idx] = grab_num + 1

        routes.append(AtomRoute(
            atom_id=atom_id,
            output_atom_type=out_type,
            source_input_idx=source_idx,
            source_atom_type=source_type,
            grab_number=grab_num,
            glyph_visits=glyph_visits,
            needs_ungrabbed=needs_ungrabbed,
        ))

    return routes


def _trace_single_atom(out_type: AtomType,
                        reactions: Dict[Reaction, int],
                        analysis: PuzzleAnalysis
                        ) -> Tuple[AtomType, List[str], bool]:
    """Trace one output atom backwards to find source type and glyph visits.

    Returns (source_atom_type, glyph_visits, needs_ungrabbed).
    """
    # Salt from calcification
    if out_type == AtomType.SALT and reactions.get(Reaction.CALCIFICATION, 0) > 0:
        # Source is whichever cardinal the input has
        for elem in [AtomType.AIR, AtomType.EARTH, AtomType.FIRE, AtomType.WATER]:
            if elem in analysis.input_elements:
                return (elem, ['glyph-calcification'], False)

    # Vitae/Mors from animismus
    if out_type in (AtomType.VITAE, AtomType.MORS):
        if reactions.get(Reaction.ANIMISMUS, 0) > 0:
            return (AtomType.SALT, ['glyph-life-and-death'], True)

    # Metal from projection
    if out_type.is_metal and reactions.get(Reaction.PROJECTION, 0) > 0:
        return (AtomType.QUICKSILVER, ['glyph-projection'], False)

    # Cardinal from Van Berlo
    if out_type.is_cardinal and reactions.get(Reaction.VAN_BERLO, 0) > 0:
        if out_type not in analysis.input_elements:
            return (AtomType.SALT, ['glyph-duplication'], False)

    # Direct: same type available in input
    if out_type in analysis.input_elements:
        return (out_type, [], False)

    # Fallback: if deficit but no clear reaction, return the type itself
    return (out_type, [], False)


def _find_input_for_type(atom_type: AtomType,
                          input_elem_to_idx: Dict[AtomType, List[int]],
                          puzzle: Puzzle) -> Optional[int]:
    """Find an input io_index that provides the given atom type."""
    if atom_type in input_elem_to_idx:
        return input_elem_to_idx[atom_type][0]

    # For non-monoatomic inputs, search all inputs
    for pio in puzzle.inputs:
        for atom in pio.molecule.atoms:
            if atom.atom_type == atom_type:
                return pio.index

    return None


# ---------------------------------------------------------------------------
# Step 2: Input schedule
# ---------------------------------------------------------------------------

def _compute_input_schedule(routes: List[AtomRoute],
                            puzzle: Puzzle) -> List[InputSchedule]:
    """Count grabs per input index to build the schedule."""
    grabs: Dict[int, int] = {}
    types: Dict[int, AtomType] = {}

    for route in routes:
        idx = route.source_input_idx
        grabs[idx] = grabs.get(idx, 0) + 1
        types[idx] = route.source_atom_type

    schedule = []
    for idx in sorted(grabs.keys()):
        schedule.append(InputSchedule(
            input_idx=idx,
            atom_type=types[idx],
            grabs_per_cycle=grabs[idx],
        ))

    return schedule


# ---------------------------------------------------------------------------
# Step 3: Assembly order
# ---------------------------------------------------------------------------

def _compute_assembly_order(molecule) -> List[int]:
    """BFS from a leaf atom to determine bond-compatible delivery order.

    For a linear chain A-B-C, returns an order like [0, 1, 2] so bonds
    form correctly as atoms are delivered.
    """
    atoms = molecule.atoms
    bonds = molecule.bonds
    n = len(atoms)

    if n <= 1:
        return list(range(n))

    # Build adjacency from bonds (using atom indices)
    pos_to_idx = {atom.position: i for i, atom in enumerate(atoms)}
    adj: Dict[int, List[int]] = {i: [] for i in range(n)}

    for bond in bonds:
        fi = pos_to_idx.get(bond.from_pos)
        ti = pos_to_idx.get(bond.to_pos)
        if fi is not None and ti is not None:
            adj[fi].append(ti)
            adj[ti].append(fi)

    # Find leaf nodes (degree 1) as starting candidates
    leaves = [i for i in range(n) if len(adj[i]) <= 1]
    if not leaves:
        leaves = [0]

    # BFS from first leaf
    start = leaves[0]
    visited = set()
    order = []
    queue = [start]
    visited.add(start)

    while queue:
        node = queue.pop(0)
        order.append(node)
        for neighbor in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    # Add any unvisited atoms
    for i in range(n):
        if i not in visited:
            order.append(i)

    return order


# ---------------------------------------------------------------------------
# Step 4: Glyph list generation
# ---------------------------------------------------------------------------

def _glyph_list_single(reactions: Dict[Reaction, int]) -> List[str]:
    """Variant A: 1 glyph instance per type (cost-min)."""
    glyphs = []
    for reaction, count in reactions.items():
        if count > 0:
            for glyph_name in REACTION_GLYPHS[reaction]:
                if glyph_name == 'baron':
                    continue
                glyphs.append(glyph_name)
    return glyphs


def _glyph_list_multi(reactions: Dict[Reaction, int]) -> List[str]:
    """Variant B: N instances = recipe count (cycle-min)."""
    glyphs = []
    for reaction, count in reactions.items():
        if count > 0:
            for glyph_name in REACTION_GLYPHS[reaction]:
                if glyph_name == 'baron':
                    continue
                glyphs.extend([glyph_name] * count)
    return glyphs


def _estimate_cost(glyph_names: List[str], analysis: PuzzleAnalysis,
                    bonder_type: str = 'bonder') -> int:
    """Estimate solution cost from glyph list."""
    from .solution import PART_COSTS
    cost = 20  # arm1
    for g in glyph_names:
        cost += PART_COSTS.get(g, 0)
    if analysis.needs_bonding:
        cost += PART_COSTS.get(bonder_type, 10)
    if analysis.needs_unbonding:
        cost += 10
    return cost


def _determine_bonder_type(puzzle: Puzzle) -> str:
    """Determine which bonder type is needed based on output bond directions.

    Regular bonder bonds in one direction (2 slots).
    bonder-speed bonds in 4 directions (4 slots).
    """
    from .puzzle import PartFlag
    for pio in puzzle.outputs:
        if len(pio.molecule.bonds) <= 1:
            continue
        # Check if bonds go in multiple directions
        bond_dirs = set()
        for bond in pio.molecule.bonds:
            dq = bond.to_pos.q - bond.from_pos.q
            dr = bond.to_pos.r - bond.from_pos.r
            bond_dirs.add((dq, dr))
        if len(bond_dirs) > 1 and puzzle.has_part(PartFlag.MULTI_BONDER):
            return 'bonder-speed'
    return 'bonder'


# ---------------------------------------------------------------------------
# Fallback plans
# ---------------------------------------------------------------------------

def _fallback_plans(puzzle: Puzzle,
                    analysis: PuzzleAnalysis) -> List[ProductionPlan]:
    """Create minimal plans when atom tracing fails."""
    recipe = analysis.recipe
    reactions = recipe.reactions if recipe else {}
    bonder_type = _determine_bonder_type(puzzle)

    # Use single-instance glyph list
    glyphs = _glyph_list_single(reactions)
    cost = _estimate_cost(glyphs, analysis, bonder_type)

    plan = ProductionPlan(
        input_schedule=[],
        glyph_names=glyphs,
        need_bonder=analysis.needs_bonding,
        need_unbonder=analysis.needs_unbonding,
        bonder_type=bonder_type,
        atom_routes=[],
        assembly_order=[],
        total_grabs=0,
        estimated_cost=cost,
    )

    plans = [plan]

    # Also try multi-instance variant
    glyphs_multi = _glyph_list_multi(reactions)
    if glyphs_multi != glyphs:
        cost_multi = _estimate_cost(glyphs_multi, analysis, bonder_type)
        plan_multi = ProductionPlan(
            input_schedule=[],
            glyph_names=glyphs_multi,
            need_bonder=analysis.needs_bonding,
            need_unbonder=analysis.needs_unbonding,
            bonder_type=bonder_type,
            atom_routes=[],
            assembly_order=[],
            total_grabs=0,
            estimated_cost=cost_multi,
        )
        plans.append(plan_multi)

    return plans
