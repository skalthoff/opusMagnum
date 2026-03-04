"""Dataflow-driven tape compiler for Opus Magnum solver.

Treats tape generation as a compilation problem: the puzzle recipe is the
"source program," the arm instruction set is the "target architecture,"
and the tape is the "compiled output."  Derives structurally correct tapes
from the delivery graph instead of guessing randomly.

Compilation passes:
  1. build_delivery_graph: trace output atoms back through recipe to inputs
  2. compile_tapes: emit arm instructions for each delivery ordering/variant
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from .puzzle import AtomType, Puzzle
from .recipe import PuzzleAnalysis, Reaction, REACTION_GLYPHS
from .layout_z3 import Layout
from .solution import Inst
from .glyph_model import get_glyph_spec


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class DeliveryTask:
    """One atom-delivery job: move an atom from source to target station."""
    task_id: int
    source_idx: int           # layout station index (input)
    target_idx: int           # layout station index (glyph/bonder/output)
    atom_type: Optional[AtomType]
    needs_ungrabbed: bool     # must drop before target fires (conversion glyphs)
    depends_on: List[int] = field(default_factory=list)  # task IDs


@dataclass
class DeliveryGraph:
    """Full delivery plan for one output cycle."""
    tasks: List[DeliveryTask]
    output_atom_count: int    # atoms needed per output cycle


# ---------------------------------------------------------------------------
# Pass 1: Build delivery graph
# ---------------------------------------------------------------------------

def _find_station_idx(layout: Layout, stype: str,
                      sdata_match=None) -> Optional[int]:
    """Find the first station index matching type (and optionally data)."""
    for i, (st, sd) in enumerate(layout.stations):
        if st == stype:
            if sdata_match is None or sd == sdata_match:
                return i
    return None


def _find_all_stations(layout: Layout, stype: str) -> List[int]:
    """Find all station indices matching type."""
    return [i for i, (st, _) in enumerate(layout.stations) if st == stype]


def _find_input_stations(layout: Layout) -> List[int]:
    """Get indices of all input stations."""
    return _find_all_stations(layout, 'input')


def _find_output_station(layout: Layout) -> Optional[int]:
    """Get index of the output station."""
    return _find_station_idx(layout, 'output')


def _find_glyph_station(layout: Layout, glyph_name: str) -> Optional[int]:
    """Get index of a specific glyph station."""
    return _find_station_idx(layout, 'glyph', glyph_name)


def _find_bonder_station(layout: Layout) -> Optional[int]:
    """Get index of bonder station."""
    return _find_station_idx(layout, 'bonder')


def build_delivery_graph(layout: Layout, analysis: PuzzleAnalysis,
                         puzzle: Puzzle) -> DeliveryGraph:
    """Trace each output atom backwards through the recipe to find its source.

    For each atom in the output:
    - If it needs a glyph transformation: create a delivery from input to
      glyph station (or to output if glyph fires on grabbed atoms)
    - If it needs bonding: delivery to bonder station
    - If direct (no transformation): delivery from input to output

    Returns a DeliveryGraph with all tasks and dependencies.
    """
    tasks: List[DeliveryTask] = []
    task_id = 0

    input_stations = _find_input_stations(layout)
    output_idx = _find_output_station(layout)
    bonder_idx = _find_bonder_station(layout)

    if output_idx is None:
        return DeliveryGraph(tasks=[], output_atom_count=0)

    # Count total output atoms needed per cycle
    output_atoms: List[Tuple[AtomType, int]] = []  # (type, count)
    for pio in puzzle.outputs:
        for atom in pio.molecule.atoms:
            output_atoms.append((atom.atom_type, pio.index))

    recipe = analysis.recipe
    reactions = recipe.reactions if recipe else {}

    # Map atom types to required reactions
    # For simplicity, we trace what each output atom needs:
    # - Salt atoms: might come from calcification of a cardinal
    # - Vitae/Mors: come from animismus (salt input)
    # - Metals: come from projection chain
    # - Cardinals: direct from input, or from Van Berlo/dispersion

    # Build input element -> station index mapping
    input_elem_to_station: Dict[AtomType, int] = {}
    for si in input_stations:
        _stype, sdata = layout.stations[si]
        # sdata is the io_index; find the element from the puzzle
        if isinstance(sdata, int) and sdata < len(puzzle.inputs):
            pio = puzzle.inputs[sdata]
            if pio.molecule.is_monoatomic:
                elem = pio.molecule.atoms[0].atom_type
                input_elem_to_station[elem] = si

    # Determine which glyph stations are conversion (need ungrabbed) vs immediate
    conversion_glyph_names = set()
    for glyph_name in _get_layout_glyph_names(layout):
        try:
            spec = get_glyph_spec(glyph_name)
            if spec.is_conversion:
                conversion_glyph_names.add(glyph_name)
        except KeyError:
            pass

    # For each output atom, create delivery task(s)
    for atom_type, _out_io_idx in output_atoms:
        source_elem = _trace_source_element(atom_type, reactions, analysis)
        source_station = _find_source_station(source_elem, input_elem_to_station,
                                               input_stations)
        if source_station is None:
            # Can't trace; skip this atom
            continue

        # Determine target station based on what transformations are needed
        glyph_name = _find_glyph_for_transform(atom_type, source_elem, reactions, layout)

        if glyph_name is not None:
            glyph_idx = _find_glyph_station(layout, glyph_name)
            if glyph_idx is not None:
                needs_ungrabbed = glyph_name in conversion_glyph_names
                tasks.append(DeliveryTask(
                    task_id=task_id,
                    source_idx=source_station,
                    target_idx=glyph_idx,
                    atom_type=source_elem,
                    needs_ungrabbed=needs_ungrabbed,
                ))
                task_id += 1
                continue

        # If bonding is needed and there's a bonder station
        if analysis.needs_bonding and bonder_idx is not None:
            tasks.append(DeliveryTask(
                task_id=task_id,
                source_idx=source_station,
                target_idx=bonder_idx,
                atom_type=source_elem,
                needs_ungrabbed=False,
            ))
            task_id += 1
            continue

        # Direct delivery: input to output
        tasks.append(DeliveryTask(
            task_id=task_id,
            source_idx=source_station,
            target_idx=output_idx,
            atom_type=source_elem,
            needs_ungrabbed=False,
        ))
        task_id += 1

    # Add dependencies: bonding tasks depend on prior atoms being placed
    # (simplified: tasks with same target depend on earlier tasks to that target)
    target_groups: Dict[int, List[int]] = {}
    for t in tasks:
        target_groups.setdefault(t.target_idx, []).append(t.task_id)
    for target_idx, task_ids in target_groups.items():
        for i in range(1, len(task_ids)):
            tasks[task_ids[i]].depends_on.append(task_ids[i - 1])

    return DeliveryGraph(tasks=tasks, output_atom_count=len(output_atoms))


def _get_layout_glyph_names(layout: Layout) -> List[str]:
    """Get all glyph names from layout stations."""
    return [sd for st, sd in layout.stations if st == 'glyph']


def _trace_source_element(atom_type: AtomType,
                          reactions: Dict[Reaction, int],
                          analysis: PuzzleAnalysis) -> AtomType:
    """Trace backwards: what input element produces this output element?

    For example:
    - Salt output + calcification reaction -> source is a cardinal element
    - Vitae/Mors output + animismus -> source is salt
    - Metal output + projection -> source could be quicksilver or prev metal
    """
    # Salt from calcification
    if atom_type == AtomType.SALT and Reaction.CALCIFICATION in reactions:
        # Source is whichever cardinal the input has
        for elem in [AtomType.AIR, AtomType.EARTH, AtomType.FIRE, AtomType.WATER]:
            if elem in analysis.input_elements:
                return elem

    # Vitae/Mors from animismus
    if atom_type in (AtomType.VITAE, AtomType.MORS) and Reaction.ANIMISMUS in reactions:
        return AtomType.SALT

    # Metal from projection (quicksilver + prev metal)
    if atom_type.is_metal and Reaction.PROJECTION in reactions:
        return AtomType.QUICKSILVER

    # Cardinal from Van Berlo
    if atom_type.is_cardinal and Reaction.VAN_BERLO in reactions:
        return AtomType.SALT

    # Direct: source is same as output
    return atom_type


def _find_source_station(elem: AtomType,
                         elem_to_station: Dict[AtomType, int],
                         input_stations: List[int]) -> Optional[int]:
    """Find the input station that provides the given element."""
    if elem in elem_to_station:
        return elem_to_station[elem]
    # Fallback: first input station
    return input_stations[0] if input_stations else None


def _find_glyph_for_transform(atom_type: AtomType, source_elem: AtomType,
                              reactions: Dict[Reaction, int],
                              layout: Layout) -> Optional[str]:
    """Determine which glyph is needed to transform source_elem -> atom_type."""
    if source_elem == atom_type:
        return None  # No transformation needed

    # Calcification: cardinal -> salt
    if source_elem.is_cardinal and atom_type == AtomType.SALT:
        if Reaction.CALCIFICATION in reactions:
            glyph = 'glyph-calcification'
            if _find_glyph_station(layout, glyph) is not None:
                return glyph

    # Animismus: salt -> vitae/mors
    if source_elem == AtomType.SALT and atom_type in (AtomType.VITAE, AtomType.MORS):
        if Reaction.ANIMISMUS in reactions:
            glyph = 'glyph-life-and-death'
            if _find_glyph_station(layout, glyph) is not None:
                return glyph

    # Projection: quicksilver + metal -> next metal
    if source_elem == AtomType.QUICKSILVER and atom_type.is_metal:
        if Reaction.PROJECTION in reactions:
            glyph = 'glyph-projection'
            if _find_glyph_station(layout, glyph) is not None:
                return glyph

    # Purification: metal -> prev metal + quicksilver
    if source_elem.is_metal and atom_type.is_metal:
        if Reaction.PURIFICATION in reactions:
            glyph = 'glyph-purification'
            if _find_glyph_station(layout, glyph) is not None:
                return glyph

    # Van Berlo/Duplication: salt -> cardinal
    if source_elem == AtomType.SALT and atom_type.is_cardinal:
        if Reaction.VAN_BERLO in reactions:
            glyph = 'glyph-duplication'
            if _find_glyph_station(layout, glyph) is not None:
                return glyph

    return None


# ---------------------------------------------------------------------------
# Pass 2: Compile tapes
# ---------------------------------------------------------------------------

def _rotation_instructions(from_dir: int, to_dir: int) -> List[int]:
    """Emit the shortest rotation sequence between two directions.

    Returns CW or CCW rotations, whichever is shorter (or equal).
    """
    if from_dir == to_dir:
        return []
    cw_dist = (from_dir - to_dir) % 6
    ccw_dist = (to_dir - from_dir) % 6
    if cw_dist <= ccw_dist:
        return [Inst.ROTATE_CW] * cw_dist
    else:
        return [Inst.ROTATE_CCW] * ccw_dist


def _rotation_instructions_cw(from_dir: int, to_dir: int) -> List[int]:
    """Force CW rotation from from_dir to to_dir."""
    dist = (from_dir - to_dir) % 6
    if dist == 0:
        return []
    return [Inst.ROTATE_CW] * dist


def _rotation_instructions_ccw(from_dir: int, to_dir: int) -> List[int]:
    """Force CCW rotation from from_dir to to_dir."""
    dist = (to_dir - from_dir) % 6
    if dist == 0:
        return []
    return [Inst.ROTATE_CCW] * dist


def _compile_single_delivery(source_dir: int, target_dir: int,
                             needs_ungrabbed: bool,
                             arm_start_dir: int) -> List[List[int]]:
    """Strategy 1: Single-delivery loop.

    Generate tapes for delivering one atom per cycle from source to target.
    Tries both CW and CCW paths, plus Reset and Repeat terminals.
    """
    tapes: List[List[int]] = []

    # Navigate from arm start to source
    nav_to_source = _rotation_instructions(arm_start_dir, source_dir)

    for rotate_fn in [_rotation_instructions, _rotation_instructions_cw,
                      _rotation_instructions_ccw]:
        nav_to_target = rotate_fn(source_dir, target_dir)
        if not nav_to_target and source_dir != target_dir:
            continue

        # GRX: grab, rotate to target, reset (auto-drops)
        if not needs_ungrabbed:
            tape = nav_to_source + [Inst.GRAB] + nav_to_target + [Inst.RESET]
            tapes.append(tape)

        # GRgX: grab, rotate to target, explicit drop, reset
        tape = nav_to_source + [Inst.GRAB] + nav_to_target + [Inst.DROP, Inst.RESET]
        tapes.append(tape)

        # GRgC: grab, rotate, drop, repeat (tight loop)
        if not nav_to_source:  # Only if arm starts at source
            tape = [Inst.GRAB] + nav_to_target + [Inst.DROP, Inst.REPEAT]
            tapes.append(tape)

        # GRg...C: grab, rotate to target, drop, return to source, repeat
        nav_return = _rotation_instructions(target_dir, source_dir)
        tape = (nav_to_source + [Inst.GRAB] + nav_to_target + [Inst.DROP]
                + nav_return + [Inst.REPEAT])
        tapes.append(tape)

    return tapes


def _compile_multi_delivery(tasks: List[DeliveryTask],
                            layout: Layout) -> List[List[int]]:
    """Strategy 2: Multi-delivery per cycle.

    Multiple atoms delivered per tape period. For puzzles needing 2-3 deliveries.
    Tries all valid topological orderings of tasks.
    """
    tapes: List[List[int]] = []

    if not tasks:
        return tapes

    # Get valid orderings (respecting dependencies)
    orderings = _topological_orderings(tasks)

    for ordering in orderings[:6]:  # Limit to 6 orderings
        for terminal in [Inst.RESET, Inst.REPEAT]:
            for use_drop in [True, False]:
                tape: List[int] = []
                cur_dir = layout.arm_rot

                for i, task in enumerate(ordering):
                    src_dir = layout.directions[task.source_idx]
                    tgt_dir = layout.directions[task.target_idx]

                    # Navigate to source
                    tape.extend(_rotation_instructions(cur_dir, src_dir))
                    # Grab
                    tape.append(Inst.GRAB)
                    # Navigate to target
                    tape.extend(_rotation_instructions(src_dir, tgt_dir))
                    # Drop (explicit or let terminal handle it)
                    if use_drop or task.needs_ungrabbed or i < len(ordering) - 1:
                        tape.append(Inst.DROP)

                    cur_dir = tgt_dir

                # Terminal
                if terminal == Inst.REPEAT:
                    # Return to start position first
                    tape.extend(_rotation_instructions(cur_dir, layout.arm_rot))
                tape.append(terminal)
                tapes.append(tape)

    return tapes


def _compile_jiggle(source_dir: int, target_dir: int,
                    arm_start_dir: int) -> List[List[int]]:
    """Strategy 5: Jiggle pattern.

    For glyphs that fire on pass-through (calcification, bonding).
    Atom is grabbed, rotated through the glyph, and the pass-through
    triggers the glyph effect.
    """
    tapes: List[List[int]] = []

    nav_to_source = _rotation_instructions(arm_start_dir, source_dir)

    # GRrX — grab, CW, CCW, reset (jiggle through adjacent glyph)
    tape = nav_to_source + [Inst.GRAB, Inst.ROTATE_CW, Inst.ROTATE_CCW, Inst.RESET]
    tapes.append(tape)

    # GrRX — grab, CCW, CW, reset (mirror jiggle)
    tape = nav_to_source + [Inst.GRAB, Inst.ROTATE_CCW, Inst.ROTATE_CW, Inst.RESET]
    tapes.append(tape)

    # Asymmetric jiggles
    for n_fwd in range(1, 4):
        for n_bwd in range(1, 4):
            if n_fwd == 1 and n_bwd == 1:
                continue  # Already covered above
            tape = (nav_to_source + [Inst.GRAB]
                    + [Inst.ROTATE_CW] * n_fwd
                    + [Inst.ROTATE_CCW] * n_bwd
                    + [Inst.RESET])
            tapes.append(tape)
            tape = (nav_to_source + [Inst.GRAB]
                    + [Inst.ROTATE_CCW] * n_fwd
                    + [Inst.ROTATE_CW] * n_bwd
                    + [Inst.RESET])
            tapes.append(tape)

    return tapes


def _compile_conversion_delivery(source_dir: int, glyph_dir: int,
                                 output_dir: int,
                                 arm_start_dir: int) -> List[List[int]]:
    """Strategy 4: Conversion glyph delivery.

    For glyphs that require ungrabbed atoms (animismus, projection QS slot):
    grab from input, deliver to glyph (drop), wait, grab product from
    glyph output, deliver to output.
    """
    tapes: List[List[int]] = []

    nav_to_source = _rotation_instructions(arm_start_dir, source_dir)
    nav_to_glyph = _rotation_instructions(source_dir, glyph_dir)

    # G R*a g . R*b G R*c X
    # grab, rotate to glyph, drop, noop wait, navigate to output, grab product, reset
    for n_wait in range(0, 3):
        nav_to_output = _rotation_instructions(glyph_dir, output_dir)
        tape = (nav_to_source + [Inst.GRAB] + nav_to_glyph + [Inst.DROP]
                + [Inst.NOOP] * n_wait
                + nav_to_output
                + [Inst.GRAB] + [Inst.RESET])
        tapes.append(tape)

        # With explicit drop at output
        tape = (nav_to_source + [Inst.GRAB] + nav_to_glyph + [Inst.DROP]
                + [Inst.NOOP] * n_wait
                + nav_to_output
                + [Inst.GRAB]
                + _rotation_instructions(output_dir, output_dir)  # noop
                + [Inst.DROP, Inst.RESET])
        tapes.append(tape)

    return tapes


def _topological_orderings(tasks: List[DeliveryTask],
                           max_orderings: int = 10) -> List[List[DeliveryTask]]:
    """Generate valid topological orderings of tasks (respecting dependencies).

    Uses Kahn's algorithm with all valid orderings (up to max_orderings).
    """
    if not tasks:
        return []
    if len(tasks) == 1:
        return [tasks]

    # Build dependency graph
    in_degree: Dict[int, int] = {t.task_id: 0 for t in tasks}
    dependents: Dict[int, List[int]] = {t.task_id: [] for t in tasks}
    task_map = {t.task_id: t for t in tasks}

    for t in tasks:
        for dep_id in t.depends_on:
            if dep_id in task_map:
                in_degree[t.task_id] += 1
                dependents[dep_id].append(t.task_id)

    results: List[List[DeliveryTask]] = []

    def _generate(current: List[int], in_deg: Dict[int, int]):
        if len(results) >= max_orderings:
            return
        available = [tid for tid, deg in in_deg.items()
                     if deg == 0 and tid not in current]
        if not available:
            if len(current) == len(tasks):
                results.append([task_map[tid] for tid in current])
            return
        for tid in available:
            new_deg = dict(in_deg)
            new_deg[tid] = -1  # Mark as used
            for dep_tid in dependents[tid]:
                new_deg[dep_tid] -= 1
            _generate(current + [tid], new_deg)

    _generate([], dict(in_degree))
    return results if results else [[task_map[tid] for tid in sorted(task_map)]]


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def compile_tapes(layout: Layout, analysis: PuzzleAnalysis,
                  puzzle: Puzzle) -> List[List[int]]:
    """Compile candidate tapes from puzzle dataflow analysis.

    Generates tapes by analyzing what atoms need to flow where and
    emitting arm instructions to accomplish each delivery.

    Returns deduplicated candidate tapes (typically 10-100 per layout).
    """
    tapes: List[List[int]] = []

    # Build delivery graph
    graph = build_delivery_graph(layout, analysis, puzzle)

    input_stations = _find_input_stations(layout)
    output_idx = _find_output_station(layout)
    arm_start = layout.arm_rot

    if output_idx is None:
        return tapes

    # --- Strategy 1: Single-delivery loops ---
    # For each delivery task, generate single-delivery tapes
    for task in graph.tasks:
        src_dir = layout.directions[task.source_idx]
        tgt_dir = layout.directions[task.target_idx]

        single_tapes = _compile_single_delivery(
            src_dir, tgt_dir, task.needs_ungrabbed, arm_start)
        tapes.extend(single_tapes)

    # --- Strategy 1b: Direct input->output deliveries ---
    # Even if the graph says to go through a glyph, try direct delivery too
    # (the glyph may fire on pass-through)
    if output_idx is not None:
        out_dir = layout.directions[output_idx]
        for si in input_stations:
            inp_dir = layout.directions[si]
            single_tapes = _compile_single_delivery(
                inp_dir, out_dir, False, arm_start)
            tapes.extend(single_tapes)

    # --- Strategy 2: Multi-delivery per cycle ---
    if len(graph.tasks) >= 2:
        multi_tapes = _compile_multi_delivery(graph.tasks, layout)
        tapes.extend(multi_tapes)

    # --- Strategy 3: Repeat-based tight loops ---
    # For each unique (source, target) pair, generate repeat loops
    seen_pairs: Set[Tuple[int, int]] = set()
    for task in graph.tasks:
        pair = (task.source_idx, task.target_idx)
        if pair in seen_pairs:
            continue
        seen_pairs.add(pair)

        src_dir = layout.directions[task.source_idx]
        tgt_dir = layout.directions[task.target_idx]

        # G R*n g C (tight repeat loop)
        for rotate_fn in [_rotation_instructions, _rotation_instructions_cw,
                          _rotation_instructions_ccw]:
            nav = rotate_fn(src_dir, tgt_dir)
            if not nav and src_dir != tgt_dir:
                continue

            # Variant: grab at source, rotate, drop, repeat
            tape = [Inst.GRAB] + nav + [Inst.DROP, Inst.REPEAT]
            tapes.append(tape)

            # Variant: with setup suffix (rotate to source after repeat)
            nav_to_src = _rotation_instructions(tgt_dir, src_dir)
            if nav_to_src:
                tape = ([Inst.GRAB] + nav + [Inst.DROP, Inst.REPEAT]
                        + [Inst.NOOP] * (len(nav_to_src)) + nav_to_src)
                # The setup suffix handles positioning for the loop
                tapes.append(tape)

            # Variant: grab, rotate, implicit drop via reset
            tape = [Inst.GRAB] + nav + [Inst.RESET]
            tapes.append(tape)

    # --- Strategy 4: Conversion glyph delivery ---
    # For tasks needing ungrabbed atoms at conversion glyphs
    for task in graph.tasks:
        if not task.needs_ungrabbed:
            continue
        src_dir = layout.directions[task.source_idx]
        glyph_dir = layout.directions[task.target_idx]
        out_dir = layout.directions[output_idx]

        conv_tapes = _compile_conversion_delivery(
            src_dir, glyph_dir, out_dir, arm_start)
        tapes.extend(conv_tapes)

    # --- Strategy 5: Jiggle patterns ---
    # For immediate glyphs (calcification, bonding) that fire on pass-through
    immediate_glyphs = set()
    for st, sd in layout.stations:
        if st == 'glyph':
            try:
                spec = get_glyph_spec(sd)
                if not spec.is_conversion:
                    immediate_glyphs.add(sd)
            except KeyError:
                pass

    if immediate_glyphs:
        for si in input_stations:
            src_dir = layout.directions[si]
            jiggle_tapes = _compile_jiggle(src_dir, src_dir, arm_start)
            tapes.extend(jiggle_tapes)

    # --- Strategy 6: Stacked layout patterns ---
    # When all non-input stations share the same direction (stacked layout),
    # generate specialized tapes
    non_input_dirs = set()
    for i, (st, _) in enumerate(layout.stations):
        if st != 'input':
            non_input_dirs.add(layout.directions[i])

    if len(non_input_dirs) == 1:
        process_dir = non_input_dirs.pop()
        for si in input_stations:
            inp_dir = layout.directions[si]
            # Simple GRX for each input
            nav = _rotation_instructions(inp_dir, process_dir)
            tapes.append([Inst.GRAB] + nav + [Inst.RESET])
            tapes.append([Inst.GRAB] + nav + [Inst.DROP, Inst.RESET])

            # CW and CCW explicit variants
            nav_cw = _rotation_instructions_cw(inp_dir, process_dir)
            nav_ccw = _rotation_instructions_ccw(inp_dir, process_dir)
            if nav_cw != nav:
                tapes.append([Inst.GRAB] + nav_cw + [Inst.RESET])
                tapes.append([Inst.GRAB] + nav_cw + [Inst.DROP, Inst.RESET])
            if nav_ccw != nav:
                tapes.append([Inst.GRAB] + nav_ccw + [Inst.RESET])
                tapes.append([Inst.GRAB] + nav_ccw + [Inst.DROP, Inst.RESET])

    # --- Strategy 7: All-direction single-step deliveries ---
    # Try every possible single-rotation-count tape (brute force small space)
    for n_rot in range(1, 6):
        for rot_inst in [Inst.ROTATE_CW, Inst.ROTATE_CCW]:
            for terminal in [Inst.RESET, Inst.REPEAT]:
                tapes.append([Inst.GRAB] + [rot_inst] * n_rot + [terminal])
                tapes.append([Inst.GRAB] + [rot_inst] * n_rot
                             + [Inst.DROP, terminal])

    # --- Strategy 9: Pass-through (no DROP) ---
    # Glyph fires on held atom as arm sweeps through. RESET deposits atom
    # back at arm tip (useful for self-return layouts where input=output).
    # Also useful for any layout where the arm returns to a bonder/output.
    for si in input_stations:
        inp_dir = layout.directions[si]
        # Sweep through each glyph direction and back
        for gi, (st, sd) in enumerate(layout.stations):
            if st != 'glyph':
                continue
            glyph_dir = layout.directions[gi]

            # CW to glyph, then continue or return
            for n_extra in range(0, 4):
                # Sweep CW past glyph, then back CCW
                cw_to_glyph = _rotation_instructions_cw(inp_dir, glyph_dir)
                if cw_to_glyph:
                    tape = ([Inst.GRAB] + cw_to_glyph
                            + [Inst.ROTATE_CCW] * n_extra + [Inst.RESET])
                    tapes.append(tape)
                    tape = ([Inst.GRAB] + cw_to_glyph
                            + [Inst.ROTATE_CW] * n_extra + [Inst.RESET])
                    tapes.append(tape)

                # Sweep CCW past glyph, then back CW
                ccw_to_glyph = _rotation_instructions_ccw(inp_dir, glyph_dir)
                if ccw_to_glyph:
                    tape = ([Inst.GRAB] + ccw_to_glyph
                            + [Inst.ROTATE_CW] * n_extra + [Inst.RESET])
                    tapes.append(tape)
                    tape = ([Inst.GRAB] + ccw_to_glyph
                            + [Inst.ROTATE_CCW] * n_extra + [Inst.RESET])
                    tapes.append(tape)

        # Multi-glyph pass-through: sweep through multiple glyphs in one motion
        glyph_dirs = [layout.directions[gi]
                      for gi, (st, _) in enumerate(layout.stations)
                      if st == 'glyph']
        if len(glyph_dirs) >= 1:
            # Sweep from input through all glyphs and reset (no DROP)
            for first_dir in [Inst.ROTATE_CW, Inst.ROTATE_CCW]:
                for total_rot in range(1, 6):
                    tape = [Inst.GRAB] + [first_dir] * total_rot + [Inst.RESET]
                    tapes.append(tape)

    # --- Strategy 8: Per-atom spread delivery for multi-atom outputs ---
    atom_dirs = getattr(layout, '_atom_dirs', None)
    if atom_dirs and graph.tasks:
        _compile_spread_delivery_from_tasks(
            tapes, graph.tasks, atom_dirs, layout)

    # --- Deduplicate ---
    seen: Set[Tuple[int, ...]] = set()
    unique: List[List[int]] = []
    for tape in tapes:
        key = tuple(tape)
        if key not in seen and len(tape) >= 2:
            seen.add(key)
            unique.append(tape)

    return unique


def _compile_spread_delivery_from_tasks(
    tapes: List[List[int]],
    tasks: List[DeliveryTask],
    atom_dirs: List[int],
    layout: Layout,
) -> None:
    """Generate tapes for spread layouts using DeliveryTasks.

    Each atom_dirs[i] gives the target arm direction for task i.
    """
    arm_start = layout.arm_rot
    if len(atom_dirs) != len(tasks):
        return

    # Full delivery sequence
    for terminal in [Inst.RESET, Inst.REPEAT]:
        tape: List[int] = []
        cur_dir = arm_start

        for ti, task in enumerate(tasks):
            src_dir = layout.directions[task.source_idx]
            dest_dir = atom_dirs[ti]

            tape.extend(_rotation_instructions(cur_dir, src_dir))
            tape.append(Inst.GRAB)
            tape.extend(_rotation_instructions(src_dir, dest_dir))
            tape.append(Inst.DROP)
            cur_dir = dest_dir

        if terminal == Inst.REPEAT:
            tape.extend(_rotation_instructions(cur_dir, arm_start))
        tape.append(terminal)
        tapes.append(tape)


# ---------------------------------------------------------------------------
# Plan-aware tape compilation
# ---------------------------------------------------------------------------

def compile_tapes_from_plan(layout: Layout,
                            plan: 'ProductionPlan') -> List[List[int]]:
    """Compile tapes using a ProductionPlan's atom routes and assembly order.

    Generates tapes that handle multi-grab sequences (same input grabbed
    N times per output cycle) and assembly-ordered delivery for bonded outputs.
    """
    from .production_planner import ProductionPlan, AtomRoute

    tapes: List[List[int]] = []
    arm_start = layout.arm_rot

    input_stations = _find_input_stations(layout)
    output_idx = _find_output_station(layout)
    bonder_idx = _find_bonder_station(layout)

    if output_idx is None:
        return tapes

    # Build io_index -> station index mapping
    io_to_station: Dict[int, int] = {}
    for si in input_stations:
        _stype, sdata = layout.stations[si]
        if isinstance(sdata, int):
            io_to_station[sdata] = si

    # Find glyph stations
    glyph_stations: Dict[str, List[int]] = {}
    for i, (st, sd) in enumerate(layout.stations):
        if st == 'glyph':
            glyph_stations.setdefault(sd, []).append(i)

    routes = plan.atom_routes
    if not routes:
        return tapes

    # --- Strategy P1: Multi-grab sequential delivery ---
    # Deliver atoms in assembly order, each as a separate grab-rotate-drop-reset
    _compile_multi_grab_sequential(
        tapes, routes, plan.assembly_order, layout, arm_start,
        io_to_station, glyph_stations, bonder_idx, output_idx)

    # --- Strategy P2: Per-route single delivery loops ---
    # Each route gets its own single-delivery tape (useful when GA combines)
    _compile_per_route_singles(
        tapes, routes, layout, arm_start,
        io_to_station, glyph_stations, bonder_idx, output_idx)

    # --- Strategy P3: Multi-grab with jiggle for glyph pass-through ---
    _compile_multi_grab_jiggle(
        tapes, routes, plan.assembly_order, layout, arm_start,
        io_to_station, glyph_stations, bonder_idx, output_idx)

    # --- Deduplicate ---
    seen: Set[Tuple[int, ...]] = set()
    unique: List[List[int]] = []
    for tape in tapes:
        key = tuple(tape)
        if key not in seen and len(tape) >= 2:
            seen.add(key)
            unique.append(tape)

    return unique


def _route_source_station(route: 'AtomRoute',
                          io_to_station: Dict[int, int],
                          input_stations: List[int]) -> Optional[int]:
    """Find layout station index for a route's source input."""
    if route.source_input_idx in io_to_station:
        return io_to_station[route.source_input_idx]
    # Fallback: use first input station (for deduplicated puzzles)
    return input_stations[0] if input_stations else None


def _glyph_dirs_for_route(route: 'AtomRoute',
                           glyph_stations: Dict[str, List[int]],
                           layout: Layout) -> List[int]:
    """Get direction indices of glyphs this route should pass through."""
    dirs = []
    for glyph_name in route.glyph_visits:
        if glyph_name in glyph_stations:
            for si in glyph_stations[glyph_name]:
                dirs.append(layout.directions[si])
    return dirs


def _route_through_glyph(src_dir: int, dest_dir: int,
                           glyph_dir: int) -> List[int]:
    """Route from src to dest via glyph_dir using CW or CCW.

    Determines which rotation direction (CW or CCW) from src passes
    through glyph_dir on the way to dest, and returns that rotation sequence.
    """
    # Check if CW rotation from src hits glyph before dest
    cw_path = []
    d = src_dir
    cw_hits_glyph = False
    cw_hits_glyph_before_dest = False
    for _ in range(6):
        d = (d - 1) % 6  # CW step
        cw_path.append(d)
        if d == glyph_dir:
            cw_hits_glyph = True
            cw_hits_glyph_before_dest = True
        if d == dest_dir:
            break

    # Check CCW path
    ccw_path = []
    d = src_dir
    ccw_hits_glyph = False
    ccw_hits_glyph_before_dest = False
    for _ in range(6):
        d = (d + 1) % 6  # CCW step
        ccw_path.append(d)
        if d == glyph_dir:
            ccw_hits_glyph = True
            ccw_hits_glyph_before_dest = True
        if d == dest_dir:
            break

    # Prefer the path that passes through glyph
    if cw_hits_glyph_before_dest and not ccw_hits_glyph_before_dest:
        return [Inst.ROTATE_CW] * len(cw_path)
    elif ccw_hits_glyph_before_dest and not cw_hits_glyph_before_dest:
        return [Inst.ROTATE_CCW] * len(ccw_path)
    elif cw_hits_glyph_before_dest:
        # Both hit glyph, use shorter
        if len(cw_path) <= len(ccw_path):
            return [Inst.ROTATE_CW] * len(cw_path)
        return [Inst.ROTATE_CCW] * len(ccw_path)

    # Neither path naturally hits glyph — use shortest path
    return _rotation_instructions(src_dir, dest_dir)


def _route_avoiding_dirs(src_dir: int, dest_dir: int,
                          avoid_dirs: List[int]) -> List[int]:
    """Route from src to dest avoiding certain directions.

    Tries CW and CCW and picks the one that avoids the given directions.
    """
    avoid_set = set(avoid_dirs)

    # CW path
    cw_path = []
    d = src_dir
    cw_avoids = True
    for _ in range(6):
        d = (d - 1) % 6
        cw_path.append(d)
        if d in avoid_set and d != dest_dir:
            cw_avoids = False
        if d == dest_dir:
            break

    # CCW path
    ccw_path = []
    d = src_dir
    ccw_avoids = True
    for _ in range(6):
        d = (d + 1) % 6
        ccw_path.append(d)
        if d in avoid_set and d != dest_dir:
            ccw_avoids = False
        if d == dest_dir:
            break

    # Prefer avoiding path, then shorter
    if ccw_avoids and not cw_avoids:
        return [Inst.ROTATE_CCW] * len(ccw_path)
    elif cw_avoids and not ccw_avoids:
        return [Inst.ROTATE_CW] * len(cw_path)
    elif len(cw_path) <= len(ccw_path):
        return [Inst.ROTATE_CW] * len(cw_path)
    return [Inst.ROTATE_CCW] * len(ccw_path)


def _compile_multi_grab_sequential(
        tapes: List[List[int]],
        routes: List['AtomRoute'],
        assembly_order: List[int],
        layout: Layout,
        arm_start: int,
        io_to_station: Dict[int, int],
        glyph_stations: Dict[str, List[int]],
        bonder_idx: Optional[int],
        output_idx: int):
    """Generate multi-grab sequential tapes with route-aware rotation.

    For each atom in assembly_order:
    - Glyph routes: grab input, rotate THROUGH glyph direction to bonder/output
    - Direct routes: grab input, rotate AROUND glyph directions to bonder/output
    Each sub-delivery ends with drop + reset.
    """
    input_stations = _find_input_stations(layout)
    need_bonder = bonder_idx is not None
    route_by_id = {r.atom_id: r for r in routes}

    order = assembly_order if assembly_order else [r.atom_id for r in routes]
    order = [aid for aid in order if aid in route_by_id]
    if not order:
        return

    # Collect all glyph directions for avoidance
    all_glyph_dirs = set()
    for gname, stations in glyph_stations.items():
        for si in stations:
            all_glyph_dirs.add(layout.directions[si])

    # Determine final target for each route
    for final_target_idx in ([bonder_idx, output_idx] if need_bonder else [output_idx]):
        if final_target_idx is None:
            continue
        final_dir = layout.directions[final_target_idx]

        tape: List[int] = []
        cur_dir = arm_start
        valid = True

        for atom_id in order:
            route = route_by_id[atom_id]
            src_station = _route_source_station(route, io_to_station,
                                                 input_stations)
            if src_station is None:
                valid = False
                break

            src_dir = layout.directions[src_station]

            # Navigate to source
            tape.extend(_rotation_instructions(cur_dir, src_dir))
            tape.append(Inst.GRAB)

            if route.glyph_visits and not route.needs_ungrabbed:
                # Route THROUGH glyph on the way to final target
                glyph_dir_list = _glyph_dirs_for_route(
                    route, glyph_stations, layout)
                if glyph_dir_list:
                    nav = _route_through_glyph(
                        src_dir, final_dir, glyph_dir_list[0])
                else:
                    nav = _rotation_instructions(src_dir, final_dir)
            elif all_glyph_dirs:
                # Direct route: AVOID glyph directions
                nav = _route_avoiding_dirs(
                    src_dir, final_dir, list(all_glyph_dirs))
            else:
                nav = _rotation_instructions(src_dir, final_dir)

            tape.extend(nav)
            tape.append(Inst.DROP)
            cur_dir = final_dir

        if not valid or not tape:
            continue

        # If all atoms were delivered to the bonder, append the bonder pickup
        # phase: GRAB bonded molecule from bonder, rotate to output, DROP.
        if need_bonder and final_target_idx == bonder_idx and output_idx is not None:
            out_dir = layout.directions[output_idx]
            bonder_dir = layout.directions[bonder_idx]
            pickup_nav = _rotation_instructions(bonder_dir, out_dir)
            tape_with_pickup = tape + [Inst.GRAB] + pickup_nav + [Inst.DROP]

            tape_with_pickup.append(Inst.RESET)
            tapes.append(tape_with_pickup)

            tape_repeat_pickup = tape_with_pickup[:-1]
            tape_repeat_pickup.extend(_rotation_instructions(out_dir, arm_start))
            tape_repeat_pickup.append(Inst.REPEAT)
            tapes.append(tape_repeat_pickup)
        else:
            # Terminal: Reset
            tape.append(Inst.RESET)
            tapes.append(tape)

            # Also try with Repeat terminal
            tape_repeat = tape[:-1]  # remove Reset
            tape_repeat.extend(_rotation_instructions(cur_dir, arm_start))
            tape_repeat.append(Inst.REPEAT)
            tapes.append(tape_repeat)

    # Also try both orderings: assembly_order and reverse
    if len(order) > 1:
        for rev_order in [list(reversed(order))]:
            for final_target_idx in ([bonder_idx, output_idx] if need_bonder
                                     else [output_idx]):
                if final_target_idx is None:
                    continue
                final_dir = layout.directions[final_target_idx]

                tape = []
                cur_dir = arm_start
                valid = True

                for atom_id in rev_order:
                    route = route_by_id[atom_id]
                    src_station = _route_source_station(
                        route, io_to_station, input_stations)
                    if src_station is None:
                        valid = False
                        break
                    src_dir = layout.directions[src_station]
                    tape.extend(_rotation_instructions(cur_dir, src_dir))
                    tape.append(Inst.GRAB)

                    if route.glyph_visits and not route.needs_ungrabbed:
                        glyph_dir_list = _glyph_dirs_for_route(
                            route, glyph_stations, layout)
                        if glyph_dir_list:
                            nav = _route_through_glyph(
                                src_dir, final_dir, glyph_dir_list[0])
                        else:
                            nav = _rotation_instructions(src_dir, final_dir)
                    elif all_glyph_dirs:
                        nav = _route_avoiding_dirs(
                            src_dir, final_dir, list(all_glyph_dirs))
                    else:
                        nav = _rotation_instructions(src_dir, final_dir)

                    tape.extend(nav)
                    tape.append(Inst.DROP)
                    cur_dir = final_dir

                if valid and tape:
                    if need_bonder and final_target_idx == bonder_idx and output_idx is not None:
                        out_dir = layout.directions[output_idx]
                        bonder_dir = layout.directions[bonder_idx]
                        pickup_nav = _rotation_instructions(bonder_dir, out_dir)
                        tape = tape + [Inst.GRAB] + pickup_nav + [Inst.DROP]
                    tape.append(Inst.RESET)
                    tapes.append(tape)


def _compile_per_route_singles(
        tapes: List[List[int]],
        routes: List['AtomRoute'],
        layout: Layout,
        arm_start: int,
        io_to_station: Dict[int, int],
        glyph_stations: Dict[str, List[int]],
        bonder_idx: Optional[int],
        output_idx: int):
    """Generate individual single-delivery tapes for each route.

    For glyph routes: route through glyph to bonder/output.
    For direct routes: route to bonder/output avoiding glyphs.
    """
    input_stations = _find_input_stations(layout)
    need_bonder = bonder_idx is not None

    # Collect glyph directions for avoidance
    all_glyph_dirs = set()
    for gname, stations in glyph_stations.items():
        for si in stations:
            all_glyph_dirs.add(layout.directions[si])

    for route in routes:
        src_station = _route_source_station(route, io_to_station,
                                             input_stations)
        if src_station is None:
            continue
        src_dir = layout.directions[src_station]

        # Determine final targets to try
        final_targets = []
        if need_bonder and bonder_idx is not None:
            final_targets.append(bonder_idx)
        final_targets.append(output_idx)

        for tgt_station in final_targets:
            tgt_dir = layout.directions[tgt_station]

            if route.glyph_visits and not route.needs_ungrabbed:
                # Route through glyph to target
                glyph_dir_list = _glyph_dirs_for_route(
                    route, glyph_stations, layout)
                if glyph_dir_list:
                    nav = _route_through_glyph(
                        src_dir, tgt_dir, glyph_dir_list[0])
                else:
                    nav = _rotation_instructions(src_dir, tgt_dir)

                # Tape: grab, route through glyph, drop, reset
                tape = [Inst.GRAB] + nav + [Inst.DROP, Inst.RESET]
                tapes.append(tape)
                tape = [Inst.GRAB] + nav + [Inst.RESET]
                tapes.append(tape)
            else:
                # Direct route, avoid glyphs if any
                if all_glyph_dirs:
                    nav = _route_avoiding_dirs(
                        src_dir, tgt_dir, list(all_glyph_dirs))
                else:
                    nav = _rotation_instructions(src_dir, tgt_dir)

                tape = [Inst.GRAB] + nav + [Inst.DROP, Inst.RESET]
                tapes.append(tape)
                tape = [Inst.GRAB] + nav + [Inst.RESET]
                tapes.append(tape)

            # Also try all CW/CCW variants
            single_tapes = _compile_single_delivery(
                src_dir, tgt_dir, route.needs_ungrabbed, arm_start)
            tapes.extend(single_tapes)

            # Also try jiggle if route has glyph visits
            if route.glyph_visits and not route.needs_ungrabbed:
                jiggle_tapes = _compile_jiggle(src_dir, tgt_dir, arm_start)
                tapes.extend(jiggle_tapes)


def _compile_multi_grab_jiggle(
        tapes: List[List[int]],
        routes: List['AtomRoute'],
        assembly_order: List[int],
        layout: Layout,
        arm_start: int,
        io_to_station: Dict[int, int],
        glyph_stations: Dict[str, List[int]],
        bonder_idx: Optional[int],
        output_idx: int):
    """Generate multi-grab tapes with jiggle + route-through for glyph effects.

    For glyph routes: grab, jiggle through glyph, deliver to bonder/output.
    For direct routes: grab, route around glyph, deliver to bonder/output.
    """
    input_stations = _find_input_stations(layout)
    need_bonder = bonder_idx is not None
    route_by_id = {r.atom_id: r for r in routes}

    order = assembly_order if assembly_order else [r.atom_id for r in routes]
    order = [aid for aid in order if aid in route_by_id]
    if not order:
        return

    has_glyph_routes = any(route_by_id[aid].glyph_visits
                           for aid in order if aid in route_by_id)
    if not has_glyph_routes:
        return

    all_glyph_dirs = set()
    for gname, stations in glyph_stations.items():
        for si in stations:
            all_glyph_dirs.add(layout.directions[si])

    for final_target_idx in ([bonder_idx, output_idx] if need_bonder
                             else [output_idx]):
        if final_target_idx is None:
            continue
        final_dir = layout.directions[final_target_idx]

        for jiggle_cw in [True, False]:
            for jiggle_size in [1, 2]:
                tape: List[int] = []
                cur_dir = arm_start
                valid = True

                for atom_id in order:
                    route = route_by_id[atom_id]
                    src_station = _route_source_station(
                        route, io_to_station, input_stations)
                    if src_station is None:
                        valid = False
                        break
                    src_dir = layout.directions[src_station]

                    tape.extend(_rotation_instructions(cur_dir, src_dir))
                    tape.append(Inst.GRAB)

                    if route.glyph_visits and not route.needs_ungrabbed:
                        # Jiggle through glyph, then route to target
                        if jiggle_cw:
                            tape.extend([Inst.ROTATE_CW] * jiggle_size)
                            tape.extend([Inst.ROTATE_CCW] * jiggle_size)
                        else:
                            tape.extend([Inst.ROTATE_CCW] * jiggle_size)
                            tape.extend([Inst.ROTATE_CW] * jiggle_size)
                        # After jiggle, back at src_dir
                        tape.extend(
                            _rotation_instructions(src_dir, final_dir))
                    elif all_glyph_dirs:
                        nav = _route_avoiding_dirs(
                            src_dir, final_dir, list(all_glyph_dirs))
                        tape.extend(nav)
                    else:
                        tape.extend(
                            _rotation_instructions(src_dir, final_dir))

                    tape.append(Inst.DROP)
                    cur_dir = final_dir

                if valid and tape:
                    tape.append(Inst.RESET)
                    tapes.append(tape)


# ---------------------------------------------------------------------------
# Station-graph-aware tape compilation
# ---------------------------------------------------------------------------

def compile_tapes_from_graph(layout: Layout, graph) -> List[List[int]]:
    """Compile tapes using a positioned StationGraph.

    The graph already knows:
    - Which direction each station is at (from layout)
    - Which flows go through which glyph directions (from flow tracing)
    - What order to deliver atoms (from assembly order)

    So tape compilation becomes mechanical:
      for each flow in assembly_order:
          rotate to flow.source direction -> GRAB
          rotate through flow.via directions (through glyph)
          rotate to flow.dest direction -> DROP
      RESET
    """
    from .station_graph import StationGraph, StationID

    tapes: List[List[int]] = []
    arm_start = layout.arm_rot

    # Build StationID -> layout station index mapping
    sid_to_layout_idx: Dict = {}
    glyph_layout_used: Set[int] = set()

    for sid, station in graph.stations.items():
        for li, (stype, sdata) in enumerate(layout.stations):
            if stype != sid.kind:
                continue
            if stype == 'input' and sdata == station.io_index:
                sid_to_layout_idx[sid] = li
                break
            elif stype == 'glyph' and sdata == station.part_name:
                if li not in glyph_layout_used:
                    sid_to_layout_idx[sid] = li
                    glyph_layout_used.add(li)
                    break
            elif stype == 'bonder':
                sid_to_layout_idx[sid] = li
                break
            elif stype == 'output':
                sid_to_layout_idx[sid] = li
                break

    def _sid_dir(sid) -> Optional[int]:
        idx = sid_to_layout_idx.get(sid)
        if idx is not None and idx < len(layout.directions):
            return layout.directions[idx]
        return None

    # Get flows in assembly order
    flow_by_id = {f.flow_id: f for f in graph.flows}
    ordered_flows = [flow_by_id[fid] for fid in graph.assembly_order
                     if fid in flow_by_id]

    if not ordered_flows:
        return tapes

    # Locate the output station direction for bonder pickup use
    g1_output_dir = None
    for sid in graph.stations:
        if sid.kind == 'output':
            g1_output_dir = _sid_dir(sid)
            break

    # Locate the bonder station direction for bonder pickup use
    g1_bonder_dir = None
    for sid in graph.stations:
        if sid.kind == 'bonder':
            g1_bonder_dir = _sid_dir(sid)
            break

    # --- Strategy G1: Full assembly sequence with route-through ---
    for terminal in [Inst.RESET, Inst.REPEAT]:
        tape: List[int] = []
        cur_dir = arm_start
        valid = True
        last_dest_sid = None

        for flow in ordered_flows:
            src_dir = _sid_dir(flow.source)
            dest_dir = _sid_dir(flow.dest)
            if src_dir is None or dest_dir is None:
                valid = False
                break

            tape.extend(_rotation_instructions(cur_dir, src_dir))
            tape.append(Inst.GRAB)

            if flow.via and not flow.needs_ungrab:
                via_dirs = [_sid_dir(via) for via in flow.via]
                via_dirs = [d for d in via_dirs if d is not None]
                if via_dirs:
                    nav = _route_through_glyph(src_dir, dest_dir, via_dirs[0])
                else:
                    nav = _rotation_instructions(src_dir, dest_dir)
                tape.extend(nav)
            else:
                tape.extend(_rotation_instructions(src_dir, dest_dir))

            tape.append(Inst.DROP)
            cur_dir = dest_dir
            last_dest_sid = flow.dest

        if not valid or not tape:
            continue

        if terminal == Inst.REPEAT:
            tape.extend(_rotation_instructions(cur_dir, arm_start))
        tape.append(terminal)
        tapes.append(tape)

    # --- Strategy G1b: Standalone bonder-pickup templates ---
    # For bonded-output puzzles: generate explicit templates covering every
    # (input_dir, bonder_dir, output_dir) combination.  Template structure:
    #   GRAB + rotate(inp->bond) + DROP          (deliver atom A)
    #   rotate(bond->inp) + GRAB + rotate(inp->bond) + DROP  (deliver atom B)
    #   GRAB + rotate(bond->out) + DROP + RESET  (pickup bonded molecule)
    if graph.need_bonder and g1_bonder_dir is not None and g1_output_dir is not None:
        # Collect all unique input directions from the ordered flows
        inp_dirs: List[int] = []
        for flow in ordered_flows:
            d = _sid_dir(flow.source)
            if d is not None and d not in inp_dirs:
                inp_dirs.append(d)

        bonder_dir = g1_bonder_dir
        out_dir = g1_output_dir

        for d_in in inp_dirs:
            rot_in_to_bond = _rotation_instructions(d_in, bonder_dir)
            rot_bond_to_in = _rotation_instructions(bonder_dir, d_in)
            rot_bond_to_out = _rotation_instructions(bonder_dir, out_dir)

            # Two-atom bonder pickup template:
            #   deliver A: GRAB + rot(in->bond) + DROP
            #   return to input: rot(bond->in)
            #   deliver B: GRAB + rot(in->bond) + DROP
            #   pickup bonded: GRAB + rot(bond->out) + DROP + RESET
            tape_2a = (
                [Inst.GRAB] + rot_in_to_bond + [Inst.DROP]
                + rot_bond_to_in
                + [Inst.GRAB] + rot_in_to_bond + [Inst.DROP]
                + [Inst.GRAB] + rot_bond_to_out + [Inst.DROP, Inst.RESET]
            )
            tapes.append(tape_2a)

            # One-atom deliver then pickup:
            #   deliver A: GRAB + rot(in->bond) + DROP
            #   pickup bonded: GRAB + rot(bond->out) + DROP + RESET
            tape_1a = (
                [Inst.GRAB] + rot_in_to_bond + [Inst.DROP]
                + [Inst.GRAB] + rot_bond_to_out + [Inst.DROP, Inst.RESET]
            )
            tapes.append(tape_1a)

            # Variants starting from arm_start position
            nav_to_in = _rotation_instructions(arm_start, d_in)
            if nav_to_in:
                tape_2a_nav = (
                    nav_to_in
                    + [Inst.GRAB] + rot_in_to_bond + [Inst.DROP]
                    + rot_bond_to_in
                    + [Inst.GRAB] + rot_in_to_bond + [Inst.DROP]
                    + [Inst.GRAB] + rot_bond_to_out + [Inst.DROP, Inst.RESET]
                )
                tapes.append(tape_2a_nav)

                tape_1a_nav = (
                    nav_to_in
                    + [Inst.GRAB] + rot_in_to_bond + [Inst.DROP]
                    + [Inst.GRAB] + rot_bond_to_out + [Inst.DROP, Inst.RESET]
                )
                tapes.append(tape_1a_nav)

        # Also generate templates for multiple distinct inputs (e.g. two different inputs)
        if len(inp_dirs) >= 2:
            for d_in_a in inp_dirs:
                for d_in_b in inp_dirs:
                    if d_in_a == d_in_b:
                        continue
                    rot_a_to_bond = _rotation_instructions(d_in_a, bonder_dir)
                    rot_bond_to_b = _rotation_instructions(bonder_dir, d_in_b)
                    rot_b_to_bond = _rotation_instructions(d_in_b, bonder_dir)
                    rot_bond_to_out = _rotation_instructions(bonder_dir, out_dir)

                    tape_ab = (
                        _rotation_instructions(arm_start, d_in_a)
                        + [Inst.GRAB] + rot_a_to_bond + [Inst.DROP]
                        + rot_bond_to_b
                        + [Inst.GRAB] + rot_b_to_bond + [Inst.DROP]
                        + [Inst.GRAB] + rot_bond_to_out + [Inst.DROP, Inst.RESET]
                    )
                    tapes.append(tape_ab)

    # --- Strategy G2: Individual flow tapes (one atom per cycle) ---
    for flow in ordered_flows:
        src_dir = _sid_dir(flow.source)
        dest_dir = _sid_dir(flow.dest)
        if src_dir is None or dest_dir is None:
            continue

        if flow.via and not flow.needs_ungrab:
            via_dirs = [_sid_dir(via) for via in flow.via]
            via_dirs = [d for d in via_dirs if d is not None]
            if via_dirs:
                nav_to_dest = _route_through_glyph(
                    src_dir, dest_dir, via_dirs[0])
            else:
                nav_to_dest = _rotation_instructions(src_dir, dest_dir)
        else:
            nav_to_dest = _rotation_instructions(src_dir, dest_dir)

        nav_to_src = _rotation_instructions(arm_start, src_dir)

        # GRX
        tapes.append(nav_to_src + [Inst.GRAB] + nav_to_dest + [Inst.RESET])
        # GRgX
        tapes.append(nav_to_src + [Inst.GRAB] + nav_to_dest
                     + [Inst.DROP, Inst.RESET])
        # GRgC (repeat)
        nav_return = _rotation_instructions(dest_dir, src_dir)
        tapes.append(nav_to_src + [Inst.GRAB] + nav_to_dest
                     + [Inst.DROP] + nav_return + [Inst.REPEAT])

    # --- Strategy G3: Conversion flow (ungrab at glyph) ---
    output_dir = None
    for sid in graph.stations:
        if sid.kind == 'output':
            output_dir = _sid_dir(sid)
            break

    for flow in ordered_flows:
        if not flow.needs_ungrab or not flow.via:
            continue
        src_dir = _sid_dir(flow.source)
        glyph_dir = _sid_dir(flow.via[0])
        if src_dir is None or glyph_dir is None or output_dir is None:
            continue

        conv_tapes = _compile_conversion_delivery(
            src_dir, glyph_dir, output_dir, arm_start)
        tapes.extend(conv_tapes)

    # --- Strategy G4: Jiggle patterns for immediate glyphs ---
    for flow in ordered_flows:
        if flow.needs_ungrab or not flow.via:
            continue
        src_dir = _sid_dir(flow.source)
        if src_dir is None:
            continue

        jiggle_tapes = _compile_jiggle(src_dir, src_dir, arm_start)
        tapes.extend(jiggle_tapes)

    # --- Strategy G5: All-direction brute force ---
    for n_rot in range(1, 6):
        for rot_inst in [Inst.ROTATE_CW, Inst.ROTATE_CCW]:
            for terminal in [Inst.RESET, Inst.REPEAT]:
                tapes.append([Inst.GRAB] + [rot_inst] * n_rot + [terminal])
                tapes.append([Inst.GRAB] + [rot_inst] * n_rot
                             + [Inst.DROP, terminal])

    # --- Strategy G6: Reverse assembly order ---
    if len(ordered_flows) > 1:
        for terminal in [Inst.RESET]:
            tape_r: List[int] = []
            cur_dir_r = arm_start
            valid_r = True

            for flow in reversed(ordered_flows):
                src_dir = _sid_dir(flow.source)
                dest_dir = _sid_dir(flow.dest)
                if src_dir is None or dest_dir is None:
                    valid_r = False
                    break

                tape_r.extend(_rotation_instructions(cur_dir_r, src_dir))
                tape_r.append(Inst.GRAB)

                if flow.via and not flow.needs_ungrab:
                    via_dirs = [_sid_dir(via) for via in flow.via]
                    via_dirs = [d for d in via_dirs if d is not None]
                    if via_dirs:
                        nav = _route_through_glyph(
                            src_dir, dest_dir, via_dirs[0])
                    else:
                        nav = _rotation_instructions(src_dir, dest_dir)
                    tape_r.extend(nav)
                else:
                    tape_r.extend(_rotation_instructions(src_dir, dest_dir))

                tape_r.append(Inst.DROP)
                cur_dir_r = dest_dir

            if valid_r and tape_r:
                tape_r.append(terminal)
                tapes.append(tape_r)

    # --- Strategy G1c: 3+ input bonder interleaved templates ---
    if graph.need_bonder and g1_bonder_dir is not None and g1_output_dir is not None:
        bonder_flows = [f for f in ordered_flows if f.dest.kind == 'bonder']
        if len(bonder_flows) >= 3:
            _compile_multi_input_bonder_templates(
                tapes, bonder_flows, layout, graph, _sid_dir,
                arm_start, g1_bonder_dir, g1_output_dir)

    # --- Strategy G8: Template composition for multi-stage puzzles ---
    glyph_flows = [f for f in ordered_flows if f.via and not f.needs_ungrab]
    if glyph_flows:
        _compile_composed_multi_stage(
            tapes, ordered_flows, layout, graph, _sid_dir,
            arm_start, g1_bonder_dir, g1_output_dir)

    # --- Strategy G7: Per-atom slot delivery for spread layouts ---
    # When the layout has _atom_dirs, each output atom has its own
    # arm direction for delivery
    atom_dirs = getattr(layout, '_atom_dirs', None)
    if atom_dirs and len(atom_dirs) == len(ordered_flows):
        _compile_spread_delivery(tapes, ordered_flows, atom_dirs,
                                 layout, graph, _sid_dir)

    # --- Deduplicate ---
    seen_g: Set[Tuple[int, ...]] = set()
    unique_g: List[List[int]] = []
    for tape in tapes:
        key = tuple(tape)
        if key not in seen_g and len(tape) >= 2:
            seen_g.add(key)
            unique_g.append(tape)

    return unique_g


def _compile_spread_delivery(
    tapes: List[List[int]],
    flows,
    atom_dirs: List[int],
    layout: Layout,
    graph,
    sid_dir_fn,
) -> None:
    """Generate tapes for spread layouts where each atom goes to a specific
    arm direction (different bonder slot position).

    For each flow i, the destination direction is atom_dirs[i] instead of
    the bonder's single direction.
    """
    arm_start = layout.arm_rot

    # Full assembly sequence: deliver each atom to its specific slot
    for terminal in [Inst.RESET, Inst.REPEAT]:
        tape: List[int] = []
        cur_dir = arm_start
        valid = True

        for fi, flow in enumerate(flows):
            src_dir = sid_dir_fn(flow.source)
            dest_dir = atom_dirs[fi] if fi < len(atom_dirs) else None
            if src_dir is None or dest_dir is None:
                valid = False
                break

            # Navigate to source
            tape.extend(_rotation_instructions(cur_dir, src_dir))
            tape.append(Inst.GRAB)

            # Route through glyph if needed
            if flow.via and not flow.needs_ungrab:
                via_dirs = [sid_dir_fn(via) for via in flow.via]
                via_dirs = [d for d in via_dirs if d is not None]
                if via_dirs:
                    nav = _route_through_glyph(src_dir, dest_dir,
                                               via_dirs[0])
                else:
                    nav = _rotation_instructions(src_dir, dest_dir)
                tape.extend(nav)
            else:
                # For direct atoms (no glyph), avoid glyph directions
                glyph_dirs_all = set()
                for sid in graph.stations:
                    if sid.kind == 'glyph':
                        gd = sid_dir_fn(sid)
                        if gd is not None:
                            glyph_dirs_all.add(gd)
                if glyph_dirs_all:
                    nav = _route_avoiding_dirs(src_dir, dest_dir,
                                               list(glyph_dirs_all))
                else:
                    nav = _rotation_instructions(src_dir, dest_dir)
                tape.extend(nav)

            tape.append(Inst.DROP)
            cur_dir = dest_dir

        if not valid or not tape:
            continue

        if terminal == Inst.REPEAT:
            tape.extend(_rotation_instructions(cur_dir, arm_start))
        tape.append(terminal)
        tapes.append(tape)

    # Also try reverse order
    for terminal in [Inst.RESET]:
        tape: List[int] = []
        cur_dir = arm_start
        valid = True

        rev_flows = list(reversed(flows))
        rev_dirs = list(reversed(atom_dirs))

        for fi, flow in enumerate(rev_flows):
            src_dir = sid_dir_fn(flow.source)
            dest_dir = rev_dirs[fi] if fi < len(rev_dirs) else None
            if src_dir is None or dest_dir is None:
                valid = False
                break

            tape.extend(_rotation_instructions(cur_dir, src_dir))
            tape.append(Inst.GRAB)

            if flow.via and not flow.needs_ungrab:
                via_dirs = [sid_dir_fn(via) for via in flow.via]
                via_dirs = [d for d in via_dirs if d is not None]
                if via_dirs:
                    nav = _route_through_glyph(src_dir, dest_dir,
                                               via_dirs[0])
                else:
                    nav = _rotation_instructions(src_dir, dest_dir)
                tape.extend(nav)
            else:
                tape.extend(_rotation_instructions(src_dir, dest_dir))

            tape.append(Inst.DROP)
            cur_dir = dest_dir

        if valid and tape:
            tape.append(terminal)
            tapes.append(tape)

    # Per-atom single delivery tapes
    for fi, flow in enumerate(flows):
        src_dir = sid_dir_fn(flow.source)
        dest_dir = atom_dirs[fi] if fi < len(atom_dirs) else None
        if src_dir is None or dest_dir is None:
            continue

        if flow.via and not flow.needs_ungrab:
            via_dirs = [sid_dir_fn(via) for via in flow.via]
            via_dirs = [d for d in via_dirs if d is not None]
            if via_dirs:
                nav = _route_through_glyph(src_dir, dest_dir,
                                           via_dirs[0])
            else:
                nav = _rotation_instructions(src_dir, dest_dir)
        else:
            nav = _rotation_instructions(src_dir, dest_dir)

        nav_to_src = _rotation_instructions(arm_start, src_dir)

        tapes.append(nav_to_src + [Inst.GRAB] + nav + [Inst.RESET])
        tapes.append(nav_to_src + [Inst.GRAB] + nav
                     + [Inst.DROP, Inst.RESET])


def _compile_multi_input_bonder_templates(
    tapes: List[List[int]],
    bonder_flows: list,
    layout: Layout,
    graph,
    sid_dir_fn,
    arm_start: int,
    bonder_dir: int,
    output_dir: int,
) -> None:
    """Strategy G1c: Generate interleaved delivery templates for 3+ input
    bonder puzzles.

    Tries permutations of bonder-targeting flows with three delivery variants:
      A) sequential delivery — deliver all, then pickup bonded
      B) navigate-back — explicitly navigate to next source between deliveries
      C) grouped by source direction — group flows sharing same source dir
    Caps total output at 100 templates.
    """
    n = len(bonder_flows)
    cap = 100
    count = 0

    # Determine which permutations to try based on flow count
    if n <= 4:
        # All permutations (up to 24)
        perms = list(itertools.permutations(bonder_flows))
    elif n <= 6:
        # Cap at 30 permutations
        perms = list(itertools.islice(itertools.permutations(bonder_flows), 30))
    else:
        # Forward + reverse only for 7+
        perms = [tuple(bonder_flows), tuple(reversed(bonder_flows))]

    rot_bond_to_out = _rotation_instructions(bonder_dir, output_dir)

    for perm in perms:
        if count >= cap:
            break

        # --- Variant A: Sequential delivery ---
        # Deliver each flow to bonder, then pickup bonded to output
        tape_a: List[int] = []
        cur_dir = arm_start
        valid = True

        for flow in perm:
            src_dir = sid_dir_fn(flow.source)
            if src_dir is None:
                valid = False
                break

            # Navigate to source
            tape_a.extend(_rotation_instructions(cur_dir, src_dir))
            tape_a.append(Inst.GRAB)

            # Route through glyph if via
            if flow.via and not flow.needs_ungrab:
                via_dirs = [sid_dir_fn(via) for via in flow.via]
                via_dirs = [d for d in via_dirs if d is not None]
                if via_dirs:
                    tape_a.extend(_route_through_glyph(
                        src_dir, bonder_dir, via_dirs[0]))
                else:
                    tape_a.extend(
                        _rotation_instructions(src_dir, bonder_dir))
            else:
                tape_a.extend(_rotation_instructions(src_dir, bonder_dir))

            tape_a.append(Inst.DROP)
            cur_dir = bonder_dir

        if valid and tape_a:
            # Pickup bonded molecule
            tape_a.append(Inst.GRAB)
            tape_a.extend(rot_bond_to_out)
            tape_a.append(Inst.DROP)
            tape_a.append(Inst.RESET)
            tapes.append(tape_a)
            count += 1

            # Also REPEAT variant
            if count < cap:
                tape_a_rep = tape_a[:-1]  # remove RESET
                tape_a_rep.extend(
                    _rotation_instructions(output_dir, arm_start))
                tape_a_rep.append(Inst.REPEAT)
                tapes.append(tape_a_rep)
                count += 1

        if count >= cap:
            break

        # --- Variant B: Navigate-back (explicit nav to next source) ---
        tape_b: List[int] = []
        cur_dir = arm_start
        valid = True

        for fi, flow in enumerate(perm):
            src_dir = sid_dir_fn(flow.source)
            if src_dir is None:
                valid = False
                break

            # Explicit navigation to source from current position
            nav_to_src = _rotation_instructions(cur_dir, src_dir)
            tape_b.extend(nav_to_src)
            tape_b.append(Inst.GRAB)

            # Route through glyph if via
            if flow.via and not flow.needs_ungrab:
                via_dirs = [sid_dir_fn(via) for via in flow.via]
                via_dirs = [d for d in via_dirs if d is not None]
                if via_dirs:
                    tape_b.extend(_route_through_glyph(
                        src_dir, bonder_dir, via_dirs[0]))
                else:
                    tape_b.extend(
                        _rotation_instructions(src_dir, bonder_dir))
            else:
                tape_b.extend(_rotation_instructions(src_dir, bonder_dir))

            tape_b.append(Inst.DROP)

            # Navigate back toward next source if not last
            if fi < len(perm) - 1:
                next_src = sid_dir_fn(perm[fi + 1].source)
                if next_src is not None:
                    tape_b.extend(
                        _rotation_instructions(bonder_dir, next_src))
                    cur_dir = next_src
                else:
                    cur_dir = bonder_dir
            else:
                cur_dir = bonder_dir

        if valid and tape_b:
            tape_b.append(Inst.GRAB)
            tape_b.extend(rot_bond_to_out)
            tape_b.append(Inst.DROP)
            tape_b.append(Inst.RESET)
            tapes.append(tape_b)
            count += 1

        if count >= cap:
            break

    # --- Variant C: Grouped by source direction ---
    if count < cap:
        # Group flows by source direction
        dir_groups: Dict[int, list] = {}
        for flow in bonder_flows:
            d = sid_dir_fn(flow.source)
            if d is not None:
                dir_groups.setdefault(d, []).append(flow)

        group_keys = list(dir_groups.keys())
        if len(group_keys) >= 2:
            # Try permutations of group ordering
            group_perms = list(itertools.islice(
                itertools.permutations(group_keys),
                min(24, cap - count)))

            for gp in group_perms:
                if count >= cap:
                    break
                tape_c: List[int] = []
                cur_dir = arm_start
                valid = True

                for gk in gp:
                    for flow in dir_groups[gk]:
                        src_dir = sid_dir_fn(flow.source)
                        if src_dir is None:
                            valid = False
                            break

                        tape_c.extend(
                            _rotation_instructions(cur_dir, src_dir))
                        tape_c.append(Inst.GRAB)

                        if flow.via and not flow.needs_ungrab:
                            via_dirs = [sid_dir_fn(via)
                                        for via in flow.via]
                            via_dirs = [d for d in via_dirs
                                        if d is not None]
                            if via_dirs:
                                tape_c.extend(_route_through_glyph(
                                    src_dir, bonder_dir, via_dirs[0]))
                            else:
                                tape_c.extend(_rotation_instructions(
                                    src_dir, bonder_dir))
                        else:
                            tape_c.extend(_rotation_instructions(
                                src_dir, bonder_dir))

                        tape_c.append(Inst.DROP)
                        cur_dir = bonder_dir

                    if not valid:
                        break

                if valid and tape_c:
                    tape_c.append(Inst.GRAB)
                    tape_c.extend(rot_bond_to_out)
                    tape_c.append(Inst.DROP)
                    tape_c.append(Inst.RESET)
                    tapes.append(tape_c)
                    count += 1


def _compile_composed_multi_stage(
    tapes: List[List[int]],
    ordered_flows: list,
    layout: Layout,
    graph,
    sid_dir_fn,
    arm_start: int,
    bonder_dir: Optional[int],
    output_dir: Optional[int],
) -> None:
    """Strategy G8: Template composition for multi-stage puzzles.

    Identifies flows that pass through glyphs (via non-empty) and direct flows,
    then builds composed sub-tapes:
      Stage A: input -> glyph (deliver raw atoms to conversion glyphs)
      Stage B: glyph -> bonder (deliver converted atoms to bonder)
      Stage C: bonder -> output (pickup bonded molecule)
    Composes via concatenation + RESET. Caps at 100 templates.
    """
    cap = 100
    count = 0

    glyph_flows = [f for f in ordered_flows if f.via and not f.needs_ungrab]
    direct_flows = [f for f in ordered_flows
                    if not f.via or f.needs_ungrab]

    # --- Sub-tape builders ---

    def _build_stage_a(flows: list, start_dir: int):
        """Input -> glyph: deliver atoms to their first via station."""
        tape: List[int] = []
        cur = start_dir
        for flow in flows:
            src_dir = sid_dir_fn(flow.source)
            if src_dir is None or not flow.via:
                return None, cur
            glyph_dir = sid_dir_fn(flow.via[0])
            if glyph_dir is None:
                return None, cur
            tape.extend(_rotation_instructions(cur, src_dir))
            tape.append(Inst.GRAB)
            tape.extend(_rotation_instructions(src_dir, glyph_dir))
            tape.append(Inst.DROP)
            cur = glyph_dir
        return tape, cur

    def _build_stage_b(flows: list, start_dir: int, target_dir: int):
        """Glyph -> bonder/output: pickup from glyph, deliver to target."""
        tape: List[int] = []
        cur = start_dir
        for flow in flows:
            if not flow.via:
                continue
            glyph_dir = sid_dir_fn(flow.via[0])
            if glyph_dir is None:
                return None, cur
            tape.extend(_rotation_instructions(cur, glyph_dir))
            tape.append(Inst.GRAB)
            tape.extend(_rotation_instructions(glyph_dir, target_dir))
            tape.append(Inst.DROP)
            cur = target_dir
        return tape, cur

    def _build_stage_c(start_dir: int, b_dir: int, o_dir: int):
        """Bonder -> output: pickup bonded molecule."""
        tape: List[int] = []
        tape.extend(_rotation_instructions(start_dir, b_dir))
        tape.append(Inst.GRAB)
        tape.extend(_rotation_instructions(b_dir, o_dir))
        tape.append(Inst.DROP)
        return tape, o_dir

    def _build_direct_deliveries(flows: list, start_dir: int):
        """Direct flows: source -> dest without via."""
        tape: List[int] = []
        cur = start_dir
        for flow in flows:
            src_dir = sid_dir_fn(flow.source)
            dest_dir = sid_dir_fn(flow.dest)
            if src_dir is None or dest_dir is None:
                return None, cur
            tape.extend(_rotation_instructions(cur, src_dir))
            tape.append(Inst.GRAB)
            tape.extend(_rotation_instructions(src_dir, dest_dir))
            tape.append(Inst.DROP)
            cur = dest_dir
        return tape, cur

    # --- Composition 1: A + B + C (glyph flows staged, then pickup) ---
    if glyph_flows and bonder_dir is not None and output_dir is not None:
        stage_a, end_a = _build_stage_a(glyph_flows, arm_start)
        if stage_a is not None:
            stage_b, end_b = _build_stage_b(
                glyph_flows, end_a, bonder_dir)
            if stage_b is not None:
                stage_c, end_c = _build_stage_c(
                    end_b, bonder_dir, output_dir)
                composed = stage_a + stage_b + stage_c + [Inst.RESET]
                tapes.append(composed)
                count += 1

                # REPEAT variant
                if count < cap:
                    rep = (stage_a + stage_b + stage_c
                           + _rotation_instructions(end_c, arm_start)
                           + [Inst.REPEAT])
                    tapes.append(rep)
                    count += 1

    # --- Composition 2: Direct flows + glyph flows interleaved ---
    if direct_flows and glyph_flows and count < cap:
        # Direct first, then glyph stages
        direct_tape, end_d = _build_direct_deliveries(
            direct_flows, arm_start)
        if direct_tape is not None:
            stage_a, end_a = _build_stage_a(glyph_flows, end_d)
            if stage_a is not None:
                dest_dir_final = output_dir if output_dir is not None \
                    else sid_dir_fn(glyph_flows[-1].dest)
                if dest_dir_final is not None:
                    stage_b, end_b = _build_stage_b(
                        glyph_flows, end_a, dest_dir_final)
                    if stage_b is not None:
                        composed = (direct_tape + stage_a + stage_b
                                    + [Inst.RESET])
                        tapes.append(composed)
                        count += 1

        # Glyph first, then direct
        if count < cap:
            stage_a, end_a = _build_stage_a(glyph_flows, arm_start)
            if stage_a is not None:
                dest_target = bonder_dir if bonder_dir is not None \
                    else (output_dir if output_dir is not None
                          else sid_dir_fn(glyph_flows[-1].dest))
                if dest_target is not None:
                    stage_b, end_b = _build_stage_b(
                        glyph_flows, end_a, dest_target)
                    if stage_b is not None:
                        direct_tape, end_d = _build_direct_deliveries(
                            direct_flows, end_b)
                        if direct_tape is not None:
                            composed = (stage_a + stage_b + direct_tape
                                        + [Inst.RESET])
                            tapes.append(composed)
                            count += 1

    # --- Composition 3: Full multi-atom composed sequence ---
    # Deliver all atoms to glyphs, pickup all to bonder, pickup bonded
    if glyph_flows and bonder_dir is not None and output_dir is not None:
        # Try different orderings of glyph flows
        flow_orderings: list = []
        if len(glyph_flows) <= 4:
            flow_orderings = list(itertools.permutations(glyph_flows))
        elif len(glyph_flows) <= 6:
            flow_orderings = list(itertools.islice(
                itertools.permutations(glyph_flows), 30))
        else:
            flow_orderings = [
                tuple(glyph_flows), tuple(reversed(glyph_flows))]

        for ordering in flow_orderings:
            if count >= cap:
                break

            # Stage A: deliver all to glyphs
            stage_a, end_a = _build_stage_a(list(ordering), arm_start)
            if stage_a is None:
                continue

            # Stage B: pickup all from glyphs to bonder
            stage_b, end_b = _build_stage_b(
                list(ordering), end_a, bonder_dir)
            if stage_b is None:
                continue

            # Stage C: pickup bonded to output
            stage_c, end_c = _build_stage_c(
                end_b, bonder_dir, output_dir)

            composed = stage_a + stage_b + stage_c + [Inst.RESET]
            tapes.append(composed)
            count += 1

            # Also include direct flows if any
            if direct_flows and count < cap:
                direct_tape, end_dir = _build_direct_deliveries(
                    direct_flows, arm_start)
                if direct_tape is not None:
                    full = (direct_tape + stage_a + stage_b + stage_c
                            + [Inst.RESET])
                    tapes.append(full)
                    count += 1
def compile_bonding_chain_tapes(layout: Layout, analysis: PuzzleAnalysis,
                                puzzle: Puzzle) -> List[List[int]]:
    """Generate complete bonding chain tapes for bonded-output puzzles.

    For puzzles where multiple atoms must be delivered to a bonder, then
    the bonded molecule picked up and delivered to the output, generates
    complete tapes covering the entire cycle:

        [deliver atom 1 to bonder] [deliver atom 2 to bonder] ...
        [pickup bonded molecule] [deliver to output] RESET

    This is critical because partial tapes (deliver without pickup) are
    useless — the GA cannot discover the missing pickup phase through
    random mutation.
    """
    tapes: List[List[int]] = []

    if not analysis.needs_bonding:
        return tapes

    input_stations = _find_input_stations(layout)
    output_idx = _find_output_station(layout)
    bonder_idx = _find_bonder_station(layout)

    if output_idx is None or bonder_idx is None or not input_stations:
        return tapes

    bonder_dir = layout.directions[bonder_idx]
    out_dir = layout.directions[output_idx]
    arm_start = layout.arm_rot

    # Collect input directions
    input_dirs: List[Tuple[int, int]] = []  # (station_idx, direction)
    for si in input_stations:
        input_dirs.append((si, layout.directions[si]))

    # Find glyph stations for pass-through routes
    glyph_stations: List[Tuple[int, int, str]] = []  # (station_idx, direction, name)
    for i, (st, sd) in enumerate(layout.stations):
        if st == 'glyph':
            glyph_stations.append((i, layout.directions[i], sd))

    # Determine how many atoms need to be delivered to the bonder.
    # For bonded outputs, the output molecule's atom count is the delivery count.
    n_atoms_needed = 0
    for pio in puzzle.outputs:
        n_atoms_needed = max(n_atoms_needed, len(pio.molecule.atoms))

    if n_atoms_needed < 2:
        return tapes

    # Build delivery sequences for different input orderings
    # Each input may need to deliver multiple atoms (if same element repeated)

    # Case 1: All inputs are distinct — try all permutations of input delivery order
    if len(input_dirs) >= 2 and len(input_dirs) <= n_atoms_needed + 1:
        _compile_chain_permutations(
            tapes, input_dirs, n_atoms_needed, bonder_dir, out_dir,
            arm_start, glyph_stations, layout)

    # Case 2: Single input delivering multiple atoms to bonder
    if len(input_dirs) >= 1:
        _compile_chain_single_input(
            tapes, input_dirs, n_atoms_needed, bonder_dir, out_dir,
            arm_start, glyph_stations, layout)

    # Case 3: Pass-through bonding chains (no DROP at glyphs)
    # For self-return layouts where glyph fires on held atom during sweep,
    # then RESET deposits at bonder/output. Each GRAB-sweep-RESET delivers
    # one atom; the tape repeats N times for N atoms.
    if len(input_dirs) >= 1:
        for si, inp_dir in input_dirs:
            # Simple pass-through: GRAB, rotate N, RESET (repeat auto for chain)
            for n_rot in range(1, 6):
                for rot_inst in [Inst.ROTATE_CW, Inst.ROTATE_CCW]:
                    tape = [Inst.GRAB] + [rot_inst] * n_rot + [Inst.RESET]
                    tapes.append(tape)

            # Sweep-and-partial-return pass-through
            for n_out in range(1, 5):
                for n_back in range(1, 5):
                    if n_out == n_back:
                        continue
                    tapes.append(
                        [Inst.GRAB]
                        + [Inst.ROTATE_CW] * n_out
                        + [Inst.ROTATE_CCW] * n_back
                        + [Inst.RESET])
                    tapes.append(
                        [Inst.GRAB]
                        + [Inst.ROTATE_CCW] * n_out
                        + [Inst.ROTATE_CW] * n_back
                        + [Inst.RESET])

    # Deduplicate
    seen: Set[Tuple[int, ...]] = set()
    unique: List[List[int]] = []
    for tape in tapes:
        key = tuple(tape)
        if key not in seen and len(tape) >= 2:
            seen.add(key)
            unique.append(tape)

    return unique


def _compile_chain_permutations(
    tapes: List[List[int]],
    input_dirs: List[Tuple[int, int]],
    n_atoms: int,
    bonder_dir: int,
    out_dir: int,
    arm_start: int,
    glyph_stations: List[Tuple[int, int, str]],
    layout: Layout,
) -> None:
    """Generate bonding chain tapes for all permutations of distinct inputs."""
    # Build delivery sequences: assign each atom to an input
    # If more atoms than inputs, some inputs deliver multiple times
    n_inputs = len(input_dirs)

    # Generate input assignments: which input delivers which atom
    # For 2 atoms / 2 inputs: [(0,1), (1,0)]
    # For 3 atoms / 2 inputs: [(0,0,1), (0,1,0), (1,0,0), (0,1,1), (1,0,1), (1,1,0)]
    if n_atoms <= 4 and n_inputs <= 3:
        # Enumerate assignments
        assignments = list(itertools.product(range(n_inputs), repeat=n_atoms))
        # Filter: each input must appear at least once (if n_inputs <= n_atoms)
        if n_inputs <= n_atoms:
            assignments = [a for a in assignments
                           if len(set(a)) >= min(n_inputs, n_atoms)]
        # Limit to avoid explosion
        assignments = assignments[:24]
    else:
        # For larger cases, just use simple orderings
        assignments = [tuple(i % n_inputs for i in range(n_atoms))]

    glyph_dir_set = {gd for _, gd, _ in glyph_stations}

    for assignment in assignments:
        for use_glyph_passthrough in ([True, False] if glyph_stations else [False]):
            for terminal in [Inst.RESET, Inst.REPEAT]:
                for use_cw in [True, False]:
                    tape: List[int] = []
                    cur_dir = arm_start

                    # Phase 1: Deliver each atom to the bonder
                    for atom_idx in range(n_atoms):
                        inp_idx = assignment[atom_idx]
                        _, inp_dir = input_dirs[inp_idx]

                        # Navigate to input
                        tape.extend(_rotation_instructions(cur_dir, inp_dir))
                        tape.append(Inst.GRAB)

                        # Navigate to bonder (optionally through glyph)
                        if use_glyph_passthrough and glyph_stations:
                            _, glyph_dir, _ = glyph_stations[0]
                            nav = _route_through_glyph(inp_dir, bonder_dir,
                                                       glyph_dir)
                        elif use_cw:
                            nav = _rotation_instructions_cw(inp_dir, bonder_dir)
                        else:
                            nav = _rotation_instructions(inp_dir, bonder_dir)

                        tape.extend(nav)
                        tape.append(Inst.DROP)
                        cur_dir = bonder_dir

                    # Phase 2: Pickup bonded molecule and deliver to output
                    tape.append(Inst.GRAB)
                    tape.extend(_rotation_instructions(bonder_dir, out_dir))
                    tape.append(Inst.DROP)
                    cur_dir = out_dir

                    # Terminal
                    if terminal == Inst.REPEAT:
                        tape.extend(_rotation_instructions(cur_dir, arm_start))
                    tape.append(terminal)
                    tapes.append(tape)


def _compile_chain_single_input(
    tapes: List[List[int]],
    input_dirs: List[Tuple[int, int]],
    n_atoms: int,
    bonder_dir: int,
    out_dir: int,
    arm_start: int,
    glyph_stations: List[Tuple[int, int, str]],
    layout: Layout,
) -> None:
    """Generate bonding chain tapes where a single input delivers all atoms."""
    glyph_dir_set = {gd for _, gd, _ in glyph_stations}

    for _, inp_dir in input_dirs:
        rot_in_to_bond = _rotation_instructions(inp_dir, bonder_dir)
        rot_in_to_bond_cw = _rotation_instructions_cw(inp_dir, bonder_dir)
        rot_in_to_bond_ccw = _rotation_instructions_ccw(inp_dir, bonder_dir)
        rot_bond_to_in = _rotation_instructions(bonder_dir, inp_dir)
        rot_bond_to_out = _rotation_instructions(bonder_dir, out_dir)

        for rot_to_bond in [rot_in_to_bond, rot_in_to_bond_cw, rot_in_to_bond_ccw]:
            for terminal in [Inst.RESET, Inst.REPEAT]:
                # Build complete chain: deliver n_atoms, pickup, deliver to output
                tape: List[int] = []
                cur_dir = arm_start

                # Navigate to first input
                tape.extend(_rotation_instructions(cur_dir, inp_dir))

                for atom_idx in range(n_atoms):
                    tape.append(Inst.GRAB)
                    tape.extend(rot_to_bond)
                    tape.append(Inst.DROP)

                    if atom_idx < n_atoms - 1:
                        # Return to input for next atom
                        tape.extend(rot_bond_to_in)

                # Pickup bonded molecule
                tape.append(Inst.GRAB)
                tape.extend(rot_bond_to_out)
                tape.append(Inst.DROP)
                cur_dir = out_dir

                if terminal == Inst.REPEAT:
                    tape.extend(_rotation_instructions(cur_dir, arm_start))
                tape.append(terminal)
                tapes.append(tape)

        # Also try with glyph pass-through for each delivery
        if glyph_stations:
            _, glyph_dir, _ = glyph_stations[0]
            rot_in_via_glyph = _route_through_glyph(
                inp_dir, bonder_dir, glyph_dir)

            for terminal in [Inst.RESET, Inst.REPEAT]:
                tape = []
                cur_dir = arm_start
                tape.extend(_rotation_instructions(cur_dir, inp_dir))

                for atom_idx in range(n_atoms):
                    tape.append(Inst.GRAB)
                    tape.extend(rot_in_via_glyph)
                    tape.append(Inst.DROP)

                    if atom_idx < n_atoms - 1:
                        tape.extend(rot_bond_to_in)

                tape.append(Inst.GRAB)
                tape.extend(rot_bond_to_out)
                tape.append(Inst.DROP)
                cur_dir = out_dir

                if terminal == Inst.REPEAT:
                    tape.extend(_rotation_instructions(cur_dir, arm_start))
                tape.append(terminal)
                tapes.append(tape)


# ---------------------------------------------------------------------------
# Multi-arm tape compilation
# ---------------------------------------------------------------------------

def _arm_to_sub_layout(arm, parent_layout) -> Layout:
    """Build a synthetic single-arm Layout from one arm's station subset.

    Maps the arm's station_indices into a self-contained Layout with
    remapped directions, positions, and rotations.
    """
    sub_stations = []
    sub_directions = []
    sub_positions = []
    sub_glyph_rots = {}
    sub_output_rots = {}

    for new_idx, old_idx in enumerate(arm.station_indices):
        if old_idx < len(parent_layout.stations):
            sub_stations.append(parent_layout.stations[old_idx])
            sub_directions.append(parent_layout.directions[old_idx])
            sub_positions.append(parent_layout.positions[old_idx])
            if old_idx in parent_layout.glyph_rotations:
                sub_glyph_rots[new_idx] = parent_layout.glyph_rotations[old_idx]
            if old_idx in parent_layout.output_rotations:
                sub_output_rots[new_idx] = parent_layout.output_rotations[old_idx]

    return Layout(
        arm_pos=arm.arm_pos,
        arm_rot=arm.arm_rot,
        arm_len=arm.arm_len,
        arm_type=arm.arm_type,
        stations=sub_stations,
        directions=sub_directions,
        positions=sub_positions,
        glyph_rotations=sub_glyph_rots,
        output_rotations=sub_output_rots,
        cost=0,
    )


def compile_tapes_for_multi_arm(layout, analysis, puzzle) -> list:
    """Compile per-arm seed tapes for a MultiArmLayout.

    Returns seed_tapes_per_arm[arm_idx] = List[candidate_tapes].
    Each arm gets tapes compiled from its own station subset using
    existing single-arm compilation strategies.
    """
    result = []
    for arm in layout.arms:
        sub_layout = _arm_to_sub_layout(arm, layout)
        if not sub_layout.stations:
            result.append([])
            continue
        arm_tapes = compile_tapes(sub_layout, analysis, puzzle)
        result.append(arm_tapes)
    return result


# ---------------------------------------------------------------------------
# Beam search tape compiler
# ---------------------------------------------------------------------------

def beam_search_tape(layout: Layout, analysis, puzzle,
                     beam_width: int = 12, max_len: int = 30) -> List[List[int]]:
    """Build tapes instruction-by-instruction using beam search.

    Keeps top-K partial candidates, scored by angular distance from the
    current arm direction to the next required station. Produces tapes
    that respect layout geometry better than template-based approaches.

    Returns a list of complete candidate tapes.
    """
    input_stations = _find_input_stations(layout)
    output_idx = _find_output_station(layout)
    if output_idx is None or not input_stations:
        return []

    arm_start = layout.arm_rot
    out_dir = layout.directions[output_idx]

    # Candidate instructions for beam expansion
    expand_insts = [
        Inst.GRAB, Inst.DROP, Inst.ROTATE_CW, Inst.ROTATE_CCW,
        Inst.RESET, Inst.REPEAT,
    ]

    # Scoring: lower is better
    def _score_partial(tape: List[int], cur_dir: int, has_grabbed: bool,
                       has_dropped: bool) -> float:
        """Heuristic score for a partial tape."""
        score = len(tape) * 0.1  # prefer shorter tapes

        if has_grabbed and not has_dropped:
            # Holding an atom — reward being close to output
            dist_to_out = min((cur_dir - out_dir) % 6, (out_dir - cur_dir) % 6)
            score += dist_to_out * 0.5
        elif not has_grabbed:
            # Need to grab — reward being close to an input
            min_dist = 6
            for si in input_stations:
                inp_dir = layout.directions[si]
                d = min((cur_dir - inp_dir) % 6, (inp_dir - cur_dir) % 6)
                min_dist = min(min_dist, d)
            score += min_dist * 0.5

        return score

    # Initial beam: empty tape, arm at start direction
    # State: (tape, cur_dir, has_grabbed, has_dropped)
    beam = [([], arm_start, False, False)]
    complete_tapes: List[List[int]] = []

    for step in range(max_len):
        if not beam:
            break

        candidates = []
        for tape, cur_dir, has_grabbed, has_dropped in beam:
            for inst in expand_insts:
                new_tape = tape + [inst]
                new_dir = cur_dir
                new_grabbed = has_grabbed
                new_dropped = has_dropped

                if inst == Inst.ROTATE_CW:
                    new_dir = (cur_dir - 1) % 6
                elif inst == Inst.ROTATE_CCW:
                    new_dir = (cur_dir + 1) % 6
                elif inst == Inst.GRAB:
                    new_grabbed = True
                    new_dropped = False
                elif inst == Inst.DROP:
                    new_dropped = True
                    new_grabbed = False
                elif inst in (Inst.RESET, Inst.REPEAT):
                    # Terminal — complete tape
                    if has_grabbed or has_dropped:
                        complete_tapes.append(new_tape)
                    continue

                score = _score_partial(new_tape, new_dir, new_grabbed, new_dropped)
                candidates.append((score, new_tape, new_dir, new_grabbed, new_dropped))

        # Keep top beam_width candidates
        candidates.sort(key=lambda x: x[0])
        beam = [(t, d, g, dr) for _, t, d, g, dr in candidates[:beam_width]]

        if len(complete_tapes) >= beam_width * 2:
            break

    # Also add terminal to remaining beam entries
    for tape, cur_dir, has_grabbed, has_dropped in beam:
        if has_grabbed or has_dropped:
            complete_tapes.append(tape + [Inst.RESET])
            complete_tapes.append(tape + [Inst.REPEAT])

    # Deduplicate
    seen: Set[Tuple[int, ...]] = set()
    unique: List[List[int]] = []
    for tape in complete_tapes:
        key = tuple(tape)
        if key not in seen and len(tape) >= 2:
            seen.add(key)
            unique.append(tape)

    return unique


# ---------------------------------------------------------------------------
# Multi-grab bonding loop tape compiler
# ---------------------------------------------------------------------------

def compile_bonding_loop_tapes(layout, n_atoms: int) -> List[List[List[int]]]:
    """Generate multi-grab bonding tape templates for N-atom assembly.

    Returns [delivery_arm_tapes, reposition_arm_tapes] where each is a list
    of candidate tapes for that arm role.

    Delivery arm pattern: grab input, deliver to bonder, return, repeat N times.
    Reposition arm pattern: delayed grab of molecule, pivot to reposition, reset.
    """
    if not hasattr(layout, 'arms') or len(layout.arms) < 2:
        return [[], []]

    # Identify delivery arm (has input stations) and reposition arm (has output)
    delivery_arm_idx = -1
    reposition_arm_idx = -1
    for ai, arm in enumerate(layout.arms):
        has_input = any(
            layout.stations[si][0] == 'input'
            for si in arm.station_indices
            if si < len(layout.stations)
        )
        has_output = any(
            layout.stations[si][0] == 'output'
            for si in arm.station_indices
            if si < len(layout.stations)
        )
        if has_input and delivery_arm_idx == -1:
            delivery_arm_idx = ai
        if has_output and reposition_arm_idx == -1:
            reposition_arm_idx = ai

    if delivery_arm_idx == -1:
        delivery_arm_idx = 0
    if reposition_arm_idx == -1:
        reposition_arm_idx = 1 if len(layout.arms) > 1 else 0

    delivery_tapes: List[List[int]] = []
    reposition_tapes: List[List[int]] = []

    # --- Delivery arm tapes ---
    d_arm = layout.arms[delivery_arm_idx]
    input_dirs = []
    bonder_dirs = []
    for si in d_arm.station_indices:
        if si < len(layout.stations):
            stype = layout.stations[si][0]
            d = layout.directions[si]
            if stype == 'input':
                input_dirs.append(d)
            elif stype == 'bonder':
                bonder_dirs.append(d)

    if not input_dirs:
        input_dirs = [d_arm.arm_rot]
    if not bonder_dirs:
        bonder_dirs = input_dirs

    for inp_dir in input_dirs:
        for bond_dir in bonder_dirs:
            rot_to_bond = _rotation_instructions(inp_dir, bond_dir)
            rot_to_bond_cw = _rotation_instructions_cw(inp_dir, bond_dir)
            rot_to_bond_ccw = _rotation_instructions_ccw(inp_dir, bond_dir)
            rot_back = _rotation_instructions(bond_dir, inp_dir)

            for n_del in range(2, min(n_atoms + 1, 11)):
                for rot_fn_result in [rot_to_bond, rot_to_bond_cw, rot_to_bond_ccw]:
                    tape: List[int] = []
                    for di in range(n_del):
                        tape.append(Inst.GRAB)
                        tape.extend(rot_fn_result)
                        tape.append(Inst.DROP)
                        if di < n_del - 1:
                            tape.extend(rot_back)
                    tape.append(Inst.RESET)
                    delivery_tapes.append(tape)

                    tape_r = list(tape[:-1])
                    tape_r.extend(rot_back)
                    tape_r.append(Inst.REPEAT)
                    delivery_tapes.append(tape_r)

                    # Variant: one delivery uses PIVOT instead of ROTATE
                    if n_del >= 3 and len(rot_fn_result) > 0:
                        tape_p: List[int] = []
                        for di in range(n_del):
                            tape_p.append(Inst.GRAB)
                            if di == 1:
                                tape_p.append(Inst.PIVOT_CCW)
                            else:
                                tape_p.extend(rot_fn_result)
                            tape_p.append(Inst.DROP)
                            if di < n_del - 1:
                                tape_p.extend(rot_back)
                        tape_p.append(Inst.RESET)
                        delivery_tapes.append(tape_p)

    # Multi-input alternating patterns
    if len(input_dirs) >= 2 and bonder_dirs:
        bond_dir = bonder_dirs[0]
        for n_del in range(2, min(n_atoms + 1, 8)):
            tape: List[int] = []
            for di in range(n_del):
                src = input_dirs[di % len(input_dirs)]
                rot_to = _rotation_instructions(src, bond_dir)
                tape.append(Inst.GRAB)
                tape.extend(rot_to)
                tape.append(Inst.DROP)
                if di < n_del - 1:
                    next_src = input_dirs[(di + 1) % len(input_dirs)]
                    tape.extend(_rotation_instructions(bond_dir, next_src))
            tape.append(Inst.RESET)
            delivery_tapes.append(tape)

    # --- Reposition arm tapes ---
    for delay in range(0, 12, 2):
        for pivot_inst in [Inst.PIVOT_CW, Inst.PIVOT_CCW]:
            for n_pivots in range(1, 7):
                tape = [Inst.NOOP] * delay + [Inst.GRAB]
                tape.extend([pivot_inst] * n_pivots)
                tape.append(Inst.RESET)
                reposition_tapes.append(tape)

            for n_bursts in range(2, 4):
                for k in range(1, 4):
                    for gap in range(0, 4):
                        tape = [Inst.NOOP] * delay + [Inst.GRAB]
                        for bi in range(n_bursts):
                            tape.extend([pivot_inst] * k)
                            if bi < n_bursts - 1:
                                tape.extend([Inst.NOOP] * gap)
                        tape.append(Inst.RESET)
                        if len(tape) <= 40:
                            reposition_tapes.append(tape)

    # Deduplicate each
    def _dedup(tapes_list):
        seen_set: Set[Tuple[int, ...]] = set()
        out = []
        for t in tapes_list:
            key = tuple(t)
            if key not in seen_set and len(t) >= 2:
                seen_set.add(key)
                out.append(t)
        return out

    return [_dedup(delivery_tapes), _dedup(reposition_tapes)]
