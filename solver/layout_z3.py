"""Z3 constraint-based layout generation for Opus Magnum solver.

Replaces brute-force enumeration with SMT solving. Generates valid
layouts where arm sweeps CW from inputs through glyphs to outputs.
"""
from __future__ import annotations
import itertools
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set

try:
    import z3
except ImportError:
    z3 = None

from .hex import HexCoord, DIRECTIONS, ORIGIN, hex_spiral
from .puzzle import Puzzle, AtomType, PartFlag
from .solution import Solution, Part, Inst, PART_COSTS, Instruction
from .recipe import PuzzleAnalysis, REACTION_GLYPHS
from .glyph_model import (GlyphSpec, GLYPH_SPECS, local_to_world,
                           footprint_world, get_glyph_spec)


@dataclass
class LayoutConfig:
    """Configuration for layout generation."""
    min_arm_len: int = 1          # min arm length to try
    max_arm_len: int = 2          # max arm length to try
    max_layouts: int = 500        # max layouts to generate
    position_range: int = 3       # arm position range [-n, n]
    cost_bound: Optional[int] = None  # upper bound on cost for pruning
    timeout_ms: int = 10000       # Z3 solver timeout


@dataclass
class Layout:
    """A valid placement of all parts."""
    arm_pos: HexCoord
    arm_rot: int            # starting direction (0-5)
    arm_len: int            # 1, 2, or 3
    arm_type: str           # 'arm1', 'arm2', 'arm3', or 'arm6'
    stations: List[Tuple[str, object]]  # [(type, data), ...] in CW order
    directions: List[int]   # direction index for each station
    positions: List[HexCoord]  # world position for each station
    glyph_rotations: Dict[int, int]  # station_index -> glyph rotation
    output_rotations: Dict[int, int]  # station_index -> output rotation
    cost: int               # total cost of this layout

    @property
    def estimated_area(self) -> int:
        """Estimate area as number of unique hex positions occupied.

        Counts the arm base hex, all station positions, and glyph footprint
        hexes.  Used as a secondary sort key for compactness.
        """
        occupied: Set[Tuple[int, int]] = set()
        occupied.add((self.arm_pos.q, self.arm_pos.r))
        for pos in self.positions:
            occupied.add((pos.q, pos.r))
        # Add glyph/bonder footprint hexes
        for si, (stype, sdata) in enumerate(self.stations):
            if stype in ('glyph', 'bonder'):
                pos = self.positions[si]
                rot = self.glyph_rotations.get(si, 0)
                try:
                    spec = get_glyph_spec(sdata)
                    for h in footprint_world(pos, rot, spec):
                        occupied.add((h.q, h.r))
                except KeyError:
                    pass
        return len(occupied)

    def to_solution(self, puzzle: Puzzle, n_outputs: int) -> Solution:
        """Build a Solution from this layout (without arm tape)."""
        sol = Solution(puzzle_name=puzzle.name, solution_name="Z3Layout")

        for i, (stype, sdata) in enumerate(self.stations):
            pos = self.positions[i]

            if stype == 'input':
                sol.parts.append(Part(name='input', position=pos, io_index=sdata))
            elif stype == 'glyph':
                grot = self.glyph_rotations.get(i, 0)
                sol.parts.append(Part(name=sdata, position=pos, rotation=grot))
            elif stype == 'bonder':
                brot = self.glyph_rotations.get(i, 0)
                sol.parts.append(Part(name=sdata, position=pos, rotation=brot))
            elif stype == 'output':
                orot = self.output_rotations.get(i, 0)
                sol.parts.append(Part(name='out-std', position=pos,
                                      rotation=orot, io_index=0))
                for oi in range(1, n_outputs):
                    sol.parts.append(Part(name='out-std', position=pos,
                                          rotation=orot, io_index=oi))

        return sol

    def add_arm_with_tape(self, base_sol: Solution, tape: List[int]) -> Solution:
        """Copy solution and add arm with tape."""
        sol = Solution(puzzle_name=base_sol.puzzle_name,
                       solution_name=base_sol.solution_name)
        sol.parts = [Part(name=p.name, position=p.position, size=p.size,
                          rotation=p.rotation, io_index=p.io_index)
                     for p in base_sol.parts]
        arm = Part(name=self.arm_type, position=self.arm_pos,
                   size=self.arm_len, rotation=self.arm_rot)
        arm.set_tape(tape)
        sol.parts.append(arm)
        return sol


# ---------------------------------------------------------------------------
# Glyph alignment helpers
# ---------------------------------------------------------------------------

def _find_glyph_placements(tip_pos: HexCoord, glyph_name: str
                           ) -> List[Tuple[HexCoord, int]]:
    """Find all (glyph_origin, rotation) pairs that place a glyph's primary
    active/input slot at tip_pos.

    For conversion glyphs (animismus, dispersion, purification, unification),
    the first input slot must land on tip_pos.  For immediate glyphs
    (calcification, projection, duplication, bonding, unbonding), the first
    active or input slot must land on tip_pos.

    Returns a list of (glyph_origin, rotation) tuples.
    """
    try:
        spec = get_glyph_spec(glyph_name)
    except KeyError:
        # Not a standard glyph (e.g. 'baron') -- treat as single-hex at tip
        return [(tip_pos, rot) for rot in range(6)]

    # Determine the primary slot that needs to align with the arm tip.
    # For conversion glyphs, use the first input slot.
    # For immediate glyphs, use the first input slot if any, else first active.
    primary_slot = None
    if spec.input_slots:
        primary_slot = spec.input_slots[0]
    elif spec.active_slots:
        primary_slot = spec.active_slots[0]
    else:
        # No slots (e.g. equilibrium) -- just place at tip
        return [(tip_pos, rot) for rot in range(6)]

    du, dv = primary_slot.du, primary_slot.dv

    placements = []
    for rot in range(6):
        # local_to_world(origin, rot, du, dv) = origin + DIRECTIONS[rot]*du + DIRECTIONS[(rot+1)%6]*dv
        # We want: origin + DIRECTIONS[rot]*du + DIRECTIONS[(rot+1)%6]*dv = tip_pos
        # So: origin = tip_pos - DIRECTIONS[rot]*du - DIRECTIONS[(rot+1)%6]*dv
        u_dir = DIRECTIONS[rot]
        v_dir = DIRECTIONS[(rot + 1) % 6]
        origin_q = tip_pos.q - u_dir.q * du - v_dir.q * dv
        origin_r = tip_pos.r - u_dir.r * du - v_dir.r * dv
        glyph_origin = HexCoord(origin_q, origin_r)

        # Verify: the slot at (du, dv) with this rotation and origin should
        # equal tip_pos.
        check = local_to_world(glyph_origin, rot, du, dv)
        if check == tip_pos:
            placements.append((glyph_origin, rot))

    return placements


def _find_output_placements(tip_pos: HexCoord, puzzle: Puzzle
                            ) -> List[Tuple[HexCoord, int]]:
    """Find all (output_position, rotation) pairs that place the output
    molecule such that its first atom aligns with tip_pos.

    For monoatomic outputs, position = tip_pos with any rotation.
    For multi-atom outputs, we try all 6 rotations and compute the
    output position accordingly.
    """
    if not puzzle.outputs:
        return []

    mol = puzzle.outputs[0].molecule

    if mol.is_monoatomic:
        # Any rotation works; output position = tip_pos - atom's local position
        atom_pos = mol.atoms[0].position
        out_pos = HexCoord(tip_pos.q - atom_pos.q, tip_pos.r - atom_pos.r)
        return [(out_pos, rot) for rot in range(6)]

    # Multi-atom: find which atom is "first" (at 0,0 in molecule coords)
    # The output part position is the molecule origin.
    # For each rotation, the first atom at mol.atoms[0].position maps to
    # local_to_world(output_pos, rot, atom.q, atom.r)
    # We need this to equal tip_pos.
    first_atom = mol.atoms[0]
    aq, ar = first_atom.position.q, first_atom.position.r

    placements = []
    for rot in range(6):
        u_dir = DIRECTIONS[rot]
        v_dir = DIRECTIONS[(rot + 1) % 6]
        origin_q = tip_pos.q - u_dir.q * aq - v_dir.q * ar
        origin_r = tip_pos.r - u_dir.r * aq - v_dir.r * ar
        out_pos = HexCoord(origin_q, origin_r)

        check = local_to_world(out_pos, rot, aq, ar)
        if check == tip_pos:
            placements.append((out_pos, rot))

    return placements


# ---------------------------------------------------------------------------
# Bonder placement helper
# ---------------------------------------------------------------------------

def _find_bonder_placements(tip_pos: HexCoord, bonder_name: str = 'bonder'
                            ) -> List[Tuple[HexCoord, int]]:
    """Find all (bonder_origin, rotation) pairs that place one of the
    bonder's active slots at tip_pos."""
    try:
        spec = get_glyph_spec(bonder_name)
    except KeyError:
        return [(tip_pos, rot) for rot in range(6)]

    placements = []
    for slot in spec.active_slots:
        du, dv = slot.du, slot.dv
        for rot in range(6):
            u_dir = DIRECTIONS[rot]
            v_dir = DIRECTIONS[(rot + 1) % 6]
            origin_q = tip_pos.q - u_dir.q * du - v_dir.q * dv
            origin_r = tip_pos.r - u_dir.r * du - v_dir.r * dv
            bonder_origin = HexCoord(origin_q, origin_r)
            check = local_to_world(bonder_origin, rot, du, dv)
            if check == tip_pos:
                placements.append((bonder_origin, rot))

    # Deduplicate
    seen: Set[Tuple[int, int, int]] = set()
    unique = []
    for pos, rot in placements:
        key = (pos.q, pos.r, rot)
        if key not in seen:
            seen.add(key)
            unique.append((pos, rot))
    return unique


# ---------------------------------------------------------------------------
# Cost computation
# ---------------------------------------------------------------------------

def _compute_layout_cost(arm_type: str, stations: List[Tuple[str, object]],
                         need_bonder: bool) -> int:
    """Compute the gold cost of a layout."""
    cost = PART_COSTS.get(arm_type, 20)
    for stype, sdata in stations:
        if stype == 'glyph':
            cost += PART_COSTS.get(sdata, 0)
        elif stype == 'bonder':
            cost += PART_COSTS.get(sdata, 10)
    return cost


# ---------------------------------------------------------------------------
# Overlap / collision check
# ---------------------------------------------------------------------------

def _check_no_footprint_collisions(
    station_placements: List[Tuple[str, object, HexCoord, int]],
    arm_pos: HexCoord
) -> bool:
    """Check that glyph footprints, input/output positions, and arm position
    don't overlap each other. Returns True if no collisions."""
    occupied: Set[Tuple[int, int]] = set()
    # Arm base occupies its own hex
    occupied.add((arm_pos.q, arm_pos.r))

    for stype, sdata, pos, rot in station_placements:
        if stype == 'input':
            key = (pos.q, pos.r)
            if key in occupied:
                return False
            occupied.add(key)
        elif stype == 'glyph' or stype == 'bonder':
            glyph_name = sdata
            try:
                spec = get_glyph_spec(glyph_name)
                fp = footprint_world(pos, rot, spec)
            except KeyError:
                fp = [pos]
            for h in fp:
                key = (h.q, h.r)
                # Glyphs can overlap with each other in some layouts,
                # but shouldn't overlap with the arm base
                if key == (arm_pos.q, arm_pos.r):
                    return False
        elif stype == 'output':
            # Output position itself
            key = (pos.q, pos.r)
            # Outputs can overlap with glyphs in the game
            if key == (arm_pos.q, arm_pos.r):
                return False

    return True


# ---------------------------------------------------------------------------
# Main layout generation
# ---------------------------------------------------------------------------

def generate_layouts(puzzle: Puzzle, analysis: PuzzleAnalysis,
                     glyphs_needed: List[str], need_bonder: bool,
                     config: LayoutConfig = None,
                     bonder_name: str = 'bonder') -> List[Layout]:
    """Generate valid layouts using Z3 constraints.

    Uses a hybrid approach:
    1. Enumerate arm positions from a small hex grid
    2. Enumerate arm lengths (1, 2)
    3. Enumerate starting directions (0-5)
    4. For each combo, stations get CW-consecutive directions
    5. Use alignment checks for glyph/output rotations
    6. Check feasibility constraints

    Returns up to config.max_layouts valid layouts sorted by estimated cost.
    """
    if config is None:
        config = LayoutConfig()

    n_inputs = len(puzzle.inputs)

    # Build station sequence: inputs first, then glyphs, then bonder, then output
    station_types: List[Tuple[str, object]] = []
    for i in range(n_inputs):
        station_types.append(('input', i))
    for g in glyphs_needed:
        # Skip 'baron' -- it's a special arm-type part, not a glyph station
        if g == 'baron':
            continue
        station_types.append(('glyph', g))
    if need_bonder:
        station_types.append(('bonder', bonder_name))
    station_types.append(('output', 0))

    n_stations = len(station_types)

    # Can't fit more than 6 stations in one CW sweep
    if n_stations > 6:
        return []

    layouts: List[Layout] = []

    # Enumerate arm positions from a small hex spiral
    arm_positions = list(hex_spiral(ORIGIN, 2))  # 19 positions

    def _try_direction_set(dirs, arm_pos, arm_len, arm_type, start_dir,
                           base_cost, cap=None):
        """Try a single direction assignment. Appends valid layouts.

        If cap is given, stop after adding that many layouts from this call.
        Returns the number of layouts added.
        """
        added = 0

        # Check no duplicate directions (which would mean two stations
        # at the same arm tip position)
        if len(set(dirs)) != n_stations:
            return 0

        # Compute tip positions for each station
        tip_positions = []
        for d in dirs:
            tip = arm_pos
            for _ in range(arm_len):
                tip = tip + DIRECTIONS[d]
            tip_positions.append(tip)

        # Check no two input positions overlap
        input_tips = [tip_positions[i] for i in range(n_inputs)]
        if len(set(input_tips)) != len(input_tips):
            return 0

        # Now find valid glyph/bonder/output rotations for each station
        # Build per-station placement options
        station_options: List[List[Tuple[HexCoord, int]]] = []
        valid = True

        for si, (stype, sdata) in enumerate(station_types):
            tip = tip_positions[si]
            if stype == 'input':
                # Input just goes at the tip position, rotation 0
                station_options.append([(tip, 0)])
            elif stype == 'glyph':
                placements = _find_glyph_placements(tip, sdata)
                if not placements:
                    valid = False
                    break
                station_options.append(placements)
            elif stype == 'bonder':
                placements = _find_bonder_placements(tip)
                if not placements:
                    valid = False
                    break
                station_options.append(placements)
            elif stype == 'output':
                placements = _find_output_placements(tip, puzzle)
                if not placements:
                    valid = False
                    break
                station_options.append(placements)

        if not valid:
            return 0

        # Enumerate combinations of rotations across stations.
        # To keep the count manageable, limit the total combinations.
        combo_count = 1
        for opts in station_options:
            combo_count *= len(opts)
            if combo_count > 500:
                break

        if combo_count > 500:
            # Too many combos -- sample a subset
            # Pick first option for inputs, iterate over glyph/output
            # rotations only
            _generate_sampled_layouts(
                layouts, puzzle, station_types, station_options,
                tip_positions, dirs, arm_pos, arm_type, arm_len,
                start_dir, base_cost, config
            )
        else:
            # Full enumeration
            for combo in itertools.product(*station_options):
                positions = []
                glyph_rots: Dict[int, int] = {}
                output_rots: Dict[int, int] = {}

                for si, (pos, rot) in enumerate(combo):
                    positions.append(pos)
                    stype = station_types[si][0]
                    if stype == 'glyph':
                        glyph_rots[si] = rot
                    elif stype == 'bonder':
                        glyph_rots[si] = rot
                    elif stype == 'output':
                        output_rots[si] = rot

                # Build placement list for collision check
                placement_list = []
                for si, (stype, sdata) in enumerate(station_types):
                    rot = glyph_rots.get(si, output_rots.get(si, 0))
                    placement_list.append((stype, sdata, positions[si], rot))

                if not _check_no_footprint_collisions(placement_list, arm_pos):
                    continue

                layout = Layout(
                    arm_pos=arm_pos,
                    arm_rot=start_dir,
                    arm_len=arm_len,
                    arm_type=arm_type,
                    stations=list(station_types),
                    directions=dirs,
                    positions=positions,
                    glyph_rotations=glyph_rots,
                    output_rotations=output_rots,
                    cost=base_cost,
                )
                layouts.append(layout)
                added += 1

                if cap is not None and added >= cap:
                    break
                if len(layouts) >= config.max_layouts:
                    break

        return added

    # --- Main CW-sweep loop ---
    for arm_pos in arm_positions:
        for arm_len in range(config.min_arm_len, config.max_arm_len + 1):
            arm_type = 'arm1' if arm_len == 1 else ('arm3' if arm_len == 3 else 'arm2')

            # Quick cost check for branch-and-bound
            base_cost = _compute_layout_cost(arm_type, station_types, need_bonder)
            if config.cost_bound is not None and base_cost >= config.cost_bound:
                continue

            for start_dir in range(6):
                # Assign CW-consecutive directions to each station
                dirs = [(start_dir - i) % 6 for i in range(n_stations)]
                _try_direction_set(dirs, arm_pos, arm_len, arm_type,
                                   start_dir, base_cost)

                if len(layouts) >= config.max_layouts:
                    break
            if len(layouts) >= config.max_layouts:
                break

        # arm6 pass: always length 1, grabs all 6 neighbors, cost 30g
        arm6_cost = _compute_layout_cost('arm6', station_types, need_bonder)
        if config.cost_bound is None or arm6_cost < config.cost_bound:
            for start_dir in range(6):
                dirs = [(start_dir - i) % 6 for i in range(n_stations)]
                _try_direction_set(dirs, arm_pos, 1, 'arm6', start_dir,
                                   arm6_cost)
                if len(layouts) >= config.max_layouts:
                    break
        if len(layouts) >= config.max_layouts:
            break

    # --- Non-CW direction patterns (strategic alternatives) ---
    # These generate additional layouts with non-consecutive direction
    # assignments. Capped at 50 layouts per pattern to avoid explosion.
    non_cw_cap = 50

    for arm_pos in arm_positions:
        for arm_len in range(config.min_arm_len, config.max_arm_len + 1):
            arm_type = 'arm1' if arm_len == 1 else ('arm3' if arm_len == 3 else 'arm2')
            base_cost = _compute_layout_cost(arm_type, station_types, need_bonder)
            if config.cost_bound is not None and base_cost >= config.cost_bound:
                continue

            for start_dir in range(6):
                # Pattern 1: CCW (reversed) — directions = [start, start+1, start+2, ...]
                ccw_dirs = [(start_dir + i) % 6 for i in range(n_stations)]
                _try_direction_set(ccw_dirs, arm_pos, arm_len, arm_type,
                                   start_dir, base_cost, cap=non_cw_cap)

                # Pattern 2: Skip-one — directions = [start, start+2, start+4, ...]
                skip_dirs = [(start_dir + 2 * i) % 6 for i in range(n_stations)]
                _try_direction_set(skip_dirs, arm_pos, arm_len, arm_type,
                                   start_dir, base_cost, cap=non_cw_cap)

            # Pattern 3: For 3-station puzzles, evenly-spaced patterns
            if n_stations == 3:
                for pattern in ([0, 2, 4], [1, 3, 5]):
                    _try_direction_set(pattern, arm_pos, arm_len, arm_type,
                                       pattern[0], base_cost, cap=non_cw_cap)

        # arm6 non-CW patterns
        arm6_cost = _compute_layout_cost('arm6', station_types, need_bonder)
        if config.cost_bound is None or arm6_cost < config.cost_bound:
            for start_dir in range(6):
                ccw_dirs = [(start_dir + i) % 6 for i in range(n_stations)]
                _try_direction_set(ccw_dirs, arm_pos, 1, 'arm6', start_dir,
                                   arm6_cost, cap=non_cw_cap)
                skip_dirs = [(start_dir + 2 * i) % 6 for i in range(n_stations)]
                _try_direction_set(skip_dirs, arm_pos, 1, 'arm6', start_dir,
                                   arm6_cost, cap=non_cw_cap)
            if n_stations == 3:
                for pattern in ([0, 2, 4], [1, 3, 5]):
                    _try_direction_set(pattern, arm_pos, 1, 'arm6',
                                       pattern[0], arm6_cost, cap=non_cw_cap)

    # Sort by cost then estimated area (lower is better)
    layouts.sort(key=lambda l: (l.cost, l.estimated_area))

    # Limit to max_layouts
    return layouts[:config.max_layouts]


def generate_stacked_layouts(puzzle: Puzzle, analysis: PuzzleAnalysis,
                              glyphs_needed: List[str], need_bonder: bool,
                              config: LayoutConfig = None,
                              bonder_name: str = 'bonder') -> List[Layout]:
    """Generate layouts where non-input parts stack at one hex.

    In stacked layouts, all glyphs, bonder, and output share a single
    arm-tip position (the 'process hex'), while each input gets its own
    distinct arm-tip direction.  This enables very short tapes (e.g. GRX)
    because the arm only needs to rotate between input directions and the
    single process direction.
    """
    if config is None:
        config = LayoutConfig()

    n_inputs = len(puzzle.inputs)

    # Build the non-input station list
    glyph_stations: List[Tuple[str, object]] = []
    for g in glyphs_needed:
        if g == 'baron':
            continue
        glyph_stations.append(('glyph', g))

    bonder_station: List[Tuple[str, object]] = []
    if need_bonder:
        bonder_station = [('bonder', bonder_name)]

    output_station: List[Tuple[str, object]] = [('output', 0)]

    # Process stations are everything that stacks at the process hex
    process_stations = glyph_stations + bonder_station + output_station

    # Need at least 1 input and 1 process station, and total directions <= 6
    n_distinct_needed = n_inputs + 1  # inputs + 1 process direction
    if n_distinct_needed > 6 or n_inputs < 1:
        return []

    layouts: List[Layout] = []

    arm_positions = list(hex_spiral(ORIGIN, 2))

    def _try_stacked_arm(arm_pos, arm_len, arm_type):
        """Try all stacked layouts for a given arm position, length, and type."""
        all_stations = [('input', i) for i in range(n_inputs)] + process_stations
        n_stations = len(all_stations)

        base_cost = _compute_layout_cost(arm_type, all_stations, need_bonder)
        if config.cost_bound is not None and base_cost >= config.cost_bound:
            return

        for process_dir in range(6):
            process_hex = arm_pos
            for _ in range(arm_len):
                process_hex = process_hex + DIRECTIONS[process_dir]

            # Pick input directions: distinct directions != process_dir
            available_dirs = [d for d in range(6) if d != process_dir]
            if n_inputs > len(available_dirs):
                continue

            for input_dir_combo in itertools.combinations(available_dirs, n_inputs):
                input_dirs = list(input_dir_combo)
                input_hexes = []
                for d in input_dirs:
                    tip = arm_pos
                    for _ in range(arm_len):
                        tip = tip + DIRECTIONS[d]
                    input_hexes.append(tip)

                # Build direction and position lists
                directions = input_dirs + [process_dir] * len(process_stations)

                # Determine arm_rot: the first station's direction (first input)
                start_dir = input_dirs[0]

                # Now find valid placements for each process station
                # Inputs are simple (placed at their tip)
                station_options: List[List[Tuple[HexCoord, int]]] = []
                valid = True

                for si, (stype, sdata) in enumerate(all_stations):
                    if stype == 'input':
                        station_options.append([(input_hexes[si], 0)])
                    elif stype == 'glyph':
                        placements = _find_glyph_placements(process_hex, sdata)
                        if not placements:
                            valid = False
                            break
                        station_options.append(placements)
                    elif stype == 'bonder':
                        placements = _find_bonder_placements(process_hex)
                        if not placements:
                            valid = False
                            break
                        station_options.append(placements)
                    elif stype == 'output':
                        placements = _find_output_placements(process_hex, puzzle)
                        if not placements:
                            valid = False
                            break
                        station_options.append(placements)

                if not valid:
                    continue

                # Limit combination explosion
                combo_count = 1
                for opts in station_options:
                    combo_count *= len(opts)
                    if combo_count > 500:
                        break

                if combo_count > 500:
                    # Sample: pick first option for inputs, iterate process stations
                    trimmed = []
                    for si, opts in enumerate(station_options):
                        stype = all_stations[si][0]
                        if stype == 'input':
                            trimmed.append(opts[:1])
                        else:
                            # Pick up to 6 representative rotations
                            by_rot: Dict[int, Tuple[HexCoord, int]] = {}
                            for pos, rot in opts:
                                if rot not in by_rot:
                                    by_rot[rot] = (pos, rot)
                            trimmed.append(list(by_rot.values())[:6])
                    combo_iter = itertools.product(*trimmed)
                else:
                    combo_iter = itertools.product(*station_options)

                for combo in combo_iter:
                    positions = []
                    glyph_rots: Dict[int, int] = {}
                    output_rots: Dict[int, int] = {}

                    for si, (pos, rot) in enumerate(combo):
                        positions.append(pos)
                        stype = all_stations[si][0]
                        if stype == 'glyph':
                            glyph_rots[si] = rot
                        elif stype == 'bonder':
                            glyph_rots[si] = rot
                        elif stype == 'output':
                            output_rots[si] = rot

                    # Collision check -- but skip input-vs-glyph overlap
                    # (inputs must overlap with glyphs for processing)
                    placement_list = []
                    for si, (stype, sdata) in enumerate(all_stations):
                        rot = glyph_rots.get(si, output_rots.get(si, 0))
                        placement_list.append((stype, sdata, positions[si], rot))

                    # Only check arm_pos collision; allow glyph/output overlap
                    arm_collision = False
                    for stype, sdata, pos, rot in placement_list:
                        if (pos.q, pos.r) == (arm_pos.q, arm_pos.r):
                            arm_collision = True
                            break
                    if arm_collision:
                        continue

                    layout = Layout(
                        arm_pos=arm_pos,
                        arm_rot=start_dir,
                        arm_len=arm_len,
                        arm_type=arm_type,
                        stations=list(all_stations),
                        directions=directions,
                        positions=positions,
                        glyph_rotations=glyph_rots,
                        output_rotations=output_rots,
                        cost=base_cost,
                    )
                    layouts.append(layout)

                    if len(layouts) >= config.max_layouts:
                        return

    for arm_pos in arm_positions:
        for arm_len in range(config.min_arm_len, config.max_arm_len + 1):
            arm_type = 'arm1' if arm_len == 1 else ('arm3' if arm_len == 3 else 'arm2')
            _try_stacked_arm(arm_pos, arm_len, arm_type)
            if len(layouts) >= config.max_layouts:
                break

        # arm6 pass for stacked layouts
        _try_stacked_arm(arm_pos, 1, 'arm6')

        if len(layouts) >= config.max_layouts:
            break

    layouts.sort(key=lambda l: (l.cost, l.estimated_area))
    return layouts[:config.max_layouts]


def _generate_sampled_layouts(
    layouts: List[Layout],
    puzzle: Puzzle,
    station_types: List[Tuple[str, object]],
    station_options: List[List[Tuple[HexCoord, int]]],
    tip_positions: List[HexCoord],
    dirs: List[int],
    arm_pos: HexCoord,
    arm_type: str,
    arm_len: int,
    start_dir: int,
    base_cost: int,
    config: LayoutConfig,
) -> None:
    """Generate layouts by sampling from large combination spaces.

    For stations with many options, pick up to 6 representative rotations
    to keep the total product manageable.
    """
    max_per_station = 6
    trimmed_options = []
    for opts in station_options:
        if len(opts) > max_per_station:
            # Spread across rotations: pick one per distinct rotation
            by_rot: Dict[int, Tuple[HexCoord, int]] = {}
            for pos, rot in opts:
                if rot not in by_rot:
                    by_rot[rot] = (pos, rot)
            trimmed_options.append(list(by_rot.values())[:max_per_station])
        else:
            trimmed_options.append(opts)

    for combo in itertools.product(*trimmed_options):
        positions = []
        glyph_rots: Dict[int, int] = {}
        output_rots: Dict[int, int] = {}

        for si, (pos, rot) in enumerate(combo):
            positions.append(pos)
            stype = station_types[si][0]
            if stype == 'glyph':
                glyph_rots[si] = rot
            elif stype == 'bonder':
                glyph_rots[si] = rot
            elif stype == 'output':
                output_rots[si] = rot

        # Collision check
        placement_list = []
        for si, (stype, sdata) in enumerate(station_types):
            rot = glyph_rots.get(si, output_rots.get(si, 0))
            placement_list.append((stype, sdata, positions[si], rot))

        if not _check_no_footprint_collisions(placement_list, arm_pos):
            continue

        layout = Layout(
            arm_pos=arm_pos,
            arm_rot=start_dir,
            arm_len=arm_len,
            arm_type=arm_type,
            stations=list(station_types),
            directions=dirs,
            positions=positions,
            glyph_rotations=glyph_rots,
            output_rotations=output_rots,
            cost=base_cost,
        )
        layouts.append(layout)

        if len(layouts) >= config.max_layouts:
            return


# ---------------------------------------------------------------------------
# Lower-bound estimation for branch-and-bound
# ---------------------------------------------------------------------------

def compute_lower_bound(layout: Layout, analysis: PuzzleAnalysis) -> int:
    """Compute sum4 lower bound for branch-and-bound pruning.

    sum4 = cost + cycles + area + instructions
    This returns a lower bound on that sum.
    """
    cost = layout.cost

    # Minimum cycles: at least n_stations (grab + rotate through + output)
    cycles_lower = len(layout.stations)

    # For bonded outputs, we need at least 2 cycles per output atom
    # (one grab + one drop per atom, rotation may be 0 if same direction).
    # This is conservative: real solutions almost always need more.
    if analysis.needs_bonding:
        n_output_atoms = sum(analysis.output_elements.values())
        cycles_lower = max(cycles_lower, 2 * n_output_atoms)

    # Minimum area: number of unique hex positions occupied
    # Includes arm position + all station positions
    area_positions: Set[Tuple[int, int]] = set()
    area_positions.add((layout.arm_pos.q, layout.arm_pos.r))
    for pos in layout.positions:
        area_positions.add((pos.q, pos.r))
    area_lower = len(area_positions)

    # Minimum instructions: at least 3 (G R X or similar)
    instructions_lower = 3

    return cost + cycles_lower + area_lower + instructions_lower


# ---------------------------------------------------------------------------
# Bonder-output alignment check
# ---------------------------------------------------------------------------

def _check_bonder_output_alignment(
    station_types: List[Tuple[str, object]],
    positions: List[HexCoord],
    glyph_rotations: Dict[int, int],
    output_rotations: Dict[int, int],
    puzzle: Puzzle,
) -> bool:
    """Check that bonder slot positions align with output molecule bond endpoints.

    For each bond in the output molecule, both atoms at the bond endpoints
    (in world coordinates) must land on bonder active slot positions.
    Returns True if alignment is satisfied or if no bonder/output/bonds exist.
    """
    if not puzzle.outputs:
        return True

    output_mol = puzzle.outputs[0].molecule
    if not output_mol.bonds:
        return True  # No bonds to check

    # Find bonder and output station indices
    bonder_idx = None
    output_idx = None
    bonder_name = 'bonder'
    for i, (stype, sdata) in enumerate(station_types):
        if stype == 'bonder':
            bonder_idx = i
            bonder_name = sdata
        elif stype == 'output':
            output_idx = i

    if bonder_idx is None or output_idx is None:
        return True  # No bonder-output pair

    bonder_pos = positions[bonder_idx]
    bonder_rot = glyph_rotations.get(bonder_idx, 0)
    output_pos = positions[output_idx]
    output_rot = output_rotations.get(output_idx, 0)

    try:
        bonder_spec = get_glyph_spec(bonder_name)
    except KeyError:
        return True

    # Pre-compute bond world positions
    bond_keys = []
    for bond in output_mol.bonds:
        from_world = local_to_world(output_pos, output_rot,
                                     bond.from_pos.q, bond.from_pos.r)
        to_world = local_to_world(output_pos, output_rot,
                                   bond.to_pos.q, bond.to_pos.r)
        bond_keys.append(((from_world.q, from_world.r),
                          (to_world.q, to_world.r)))

    if not bond_keys:
        return True

    # Check if ANY single bonder rotation covers ALL bonds simultaneously
    for rot in range(6):
        rot_slots: Set[Tuple[int, int]] = set()
        for slot in bonder_spec.active_slots:
            sp = local_to_world(bonder_pos, rot, slot.du, slot.dv)
            rot_slots.add((sp.q, sp.r))

        all_covered = True
        for from_key, to_key in bond_keys:
            if from_key not in rot_slots or to_key not in rot_slots:
                all_covered = False
                break
        if all_covered:
            return True

    # Also accept if each bond is individually feasible (sequential bonding)
    for from_key, to_key in bond_keys:
        bond_feasible = False
        for rot in range(6):
            rot_slots2: Set[Tuple[int, int]] = set()
            for slot in bonder_spec.active_slots:
                sp = local_to_world(bonder_pos, rot, slot.du, slot.dv)
                rot_slots2.add((sp.q, sp.r))
            if from_key in rot_slots2 and to_key in rot_slots2:
                bond_feasible = True
                break
        if not bond_feasible:
            return False

    return True


# ---------------------------------------------------------------------------
# Graph-constrained layout generation
# ---------------------------------------------------------------------------

def generate_layouts_from_graph(graph, puzzle: Puzzle,
                                 analysis: PuzzleAnalysis,
                                 config: LayoutConfig = None) -> List[Layout]:
    """Generate layouts constrained by a StationGraph.

    Uses the graph's glyph list, bonder type, and slot constraints to
    generate only layouts where bonder-output alignment is satisfied.
    Combines CW-sweep, stacked, and multi-atom spread layouts.
    """
    if config is None:
        config = LayoutConfig()

    all_layouts: List[Layout] = []

    has_bonds = (puzzle.outputs and puzzle.outputs[0].molecule.bonds)

    # Generate CW-sweep layouts
    cw_layouts = generate_layouts(
        puzzle, analysis, graph.glyph_names, graph.need_bonder,
        config, bonder_name=graph.bonder_type)

    # Generate stacked layouts
    stacked_layouts = generate_stacked_layouts(
        puzzle, analysis, graph.glyph_names, graph.need_bonder,
        config, bonder_name=graph.bonder_type)

    combined = cw_layouts + stacked_layouts

    # Filter by bonder-output alignment if output has bonds
    if has_bonds and graph.need_bonder:
        for layout in combined:
            if _check_bonder_output_alignment(
                    layout.stations, layout.positions,
                    layout.glyph_rotations, layout.output_rotations,
                    puzzle):
                all_layouts.append(layout)
    else:
        all_layouts = combined

    # For multi-atom bonded outputs, generate spread layouts
    if has_bonds and graph.need_bonder:
        spread = _generate_spread_layouts(
            puzzle, analysis, graph.glyph_names,
            graph.bonder_type, config)
        all_layouts.extend(spread)

    all_layouts.sort(key=lambda l: (l.cost, l.estimated_area))
    return all_layouts[:config.max_layouts]


def _generate_spread_layouts(
    puzzle: Puzzle, analysis: PuzzleAnalysis,
    glyph_names: List[str], bonder_name: str,
    config: LayoutConfig,
) -> List[Layout]:
    """Generate layouts for multi-atom bonded outputs.

    Each output atom gets its own arm direction, so the arm can drop
    atoms at different bonder slot positions. The bonder and output
    share a position, and their rotations ensure slot alignment.
    """
    if not puzzle.outputs:
        return []

    mol = puzzle.outputs[0].molecule
    if not mol.bonds or mol.is_monoatomic:
        return []

    # Compute assembly order (BFS from leaf) - same as station_graph
    from .station_graph import _compute_assembly_order
    assembly_order = _compute_assembly_order(mol)

    n_output_atoms = len(mol.atoms)
    n_inputs = len(puzzle.inputs)
    n_glyphs = len([g for g in glyph_names if g != 'baron'])

    # Need: n_output_atoms dirs for atom delivery + n_inputs + n_glyphs <= 6
    total_needed = n_output_atoms + n_inputs + n_glyphs
    if total_needed > 6:
        return []

    layouts: List[Layout] = []
    arm_positions = list(hex_spiral(ORIGIN, 2))

    # Build list of (arm_len, arm_type) pairs to try, including arm6
    _spread_arm_variants = [
        (al, 'arm1' if al == 1 else ('arm3' if al == 3 else 'arm2'))
        for al in range(config.min_arm_len, config.max_arm_len + 1)
    ] + [(1, 'arm6')]

    for arm_pos in arm_positions:
        for arm_len, arm_type in _spread_arm_variants:

            # Compute tip positions for all 6 directions
            tips: Dict[int, HexCoord] = {}
            for d in range(6):
                tip = arm_pos
                for _ in range(arm_len):
                    tip = tip + DIRECTIONS[d]
                tips[d] = tip

            # For each output placement, check atom reachability
            for out_anchor_dir in range(6):
                out_tip = tips[out_anchor_dir]
                out_placements = _find_output_placements(out_tip, puzzle)

                for out_pos, out_rot in out_placements:
                    # Compute world positions of all output atoms
                    atom_worlds = []
                    for atom in mol.atoms:
                        wp = local_to_world(out_pos, out_rot,
                                            atom.position.q,
                                            atom.position.r)
                        atom_worlds.append(wp)

                    # Map each atom to an arm direction
                    atom_dirs: List[Optional[int]] = []
                    all_reach = True
                    used_dirs: Set[int] = set()
                    for aw in atom_worlds:
                        found_d = None
                        for d, tp in tips.items():
                            if tp == aw and d not in used_dirs:
                                found_d = d
                                break
                        if found_d is None:
                            all_reach = False
                            break
                        atom_dirs.append(found_d)
                        used_dirs.add(found_d)

                    if not all_reach:
                        continue

                    # Find bonder placements that align
                    bonder_placements_valid = []
                    for bd in used_dirs:
                        for bp, br in _find_bonder_placements(
                                tips[bd], bonder_name):
                            try:
                                spec = get_glyph_spec(bonder_name)
                            except KeyError:
                                continue
                            bslots = set()
                            for slot in spec.active_slots:
                                sp = local_to_world(bp, br,
                                                     slot.du, slot.dv)
                                bslots.add((sp.q, sp.r))

                            # Check all bonds covered
                            ok = True
                            for bond in mol.bonds:
                                f = local_to_world(
                                    out_pos, out_rot,
                                    bond.from_pos.q, bond.from_pos.r)
                                t = local_to_world(
                                    out_pos, out_rot,
                                    bond.to_pos.q, bond.to_pos.r)
                                if ((f.q, f.r) not in bslots or
                                        (t.q, t.r) not in bslots):
                                    ok = False
                                    break
                            if ok:
                                bonder_placements_valid.append((bp, br))

                    if not bonder_placements_valid:
                        continue

                    # Free directions for input and glyph stations
                    free_dirs = [d for d in range(6)
                                 if d not in used_dirs]
                    if len(free_dirs) < n_inputs + n_glyphs:
                        continue

                    # Try assigning inputs and glyphs to free dirs
                    needed = n_inputs + n_glyphs
                    for dir_combo in itertools.permutations(
                            free_dirs, needed):
                        input_dirs = list(dir_combo[:n_inputs])
                        glyph_dirs = list(dir_combo[n_inputs:])

                        # Build the station list and find placements
                        for bonder_pos, bonder_rot in \
                                bonder_placements_valid[:3]:
                            # Build stations: inputs, glyphs,
                            # bonder (at first atom dir), output
                            stations: List[Tuple[str, object]] = []
                            directions: List[int] = []
                            positions: List[HexCoord] = []
                            glyph_rots: Dict[int, int] = {}
                            output_rots: Dict[int, int] = {}

                            # Inputs
                            for ii in range(n_inputs):
                                stations.append(('input', ii))
                                directions.append(input_dirs[ii])
                                positions.append(tips[input_dirs[ii]])

                            # Glyphs
                            gi_offset = len(stations)
                            glyph_valid = True
                            for gi_idx, gname in enumerate(
                                    glyph_names):
                                if gname == 'baron':
                                    continue
                                if gi_idx >= len(glyph_dirs):
                                    glyph_valid = False
                                    break
                                gd = glyph_dirs[gi_idx]
                                gtip = tips[gd]
                                gplacements = _find_glyph_placements(
                                    gtip, gname)
                                if not gplacements:
                                    glyph_valid = False
                                    break
                                gpos, grot = gplacements[0]
                                si = len(stations)
                                stations.append(('glyph', gname))
                                directions.append(gd)
                                positions.append(gpos)
                                glyph_rots[si] = grot

                            if not glyph_valid:
                                continue

                            # Bonder
                            bsi = len(stations)
                            stations.append(('bonder', bonder_name))
                            directions.append(atom_dirs[0])
                            positions.append(bonder_pos)
                            glyph_rots[bsi] = bonder_rot

                            # Output
                            osi = len(stations)
                            stations.append(('output', 0))
                            directions.append(atom_dirs[0])
                            positions.append(out_pos)
                            output_rots[osi] = out_rot

                            # Compute cost
                            cost = PART_COSTS.get(arm_type, 20)
                            for st, sd in stations:
                                if st == 'glyph':
                                    cost += PART_COSTS.get(sd, 0)
                                elif st == 'bonder':
                                    cost += PART_COSTS.get(sd, 10)

                            if (config.cost_bound is not None and
                                    cost >= config.cost_bound):
                                continue

                            start_dir = directions[0]

                            layout = Layout(
                                arm_pos=arm_pos,
                                arm_rot=start_dir,
                                arm_len=arm_len,
                                arm_type=arm_type,
                                stations=stations,
                                directions=directions,
                                positions=positions,
                                glyph_rotations=glyph_rots,
                                output_rotations=output_rots,
                                cost=cost,
                            )
                            # Store atom delivery dirs in flow order
                            # (assembly_order maps flow index to
                            # atom index)
                            flow_dirs = [atom_dirs[assembly_order[i]]
                                         for i in range(
                                             len(assembly_order))
                                         if i < len(atom_dirs)
                                         and assembly_order[i]
                                         < len(atom_dirs)]
                            layout._atom_dirs = flow_dirs
                            layouts.append(layout)

                            if len(layouts) >= config.max_layouts:
                                return layouts

    layouts.sort(key=lambda l: (l.cost, l.estimated_area))
    return layouts[:config.max_layouts]
