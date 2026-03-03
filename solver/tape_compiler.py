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

    # --- Deduplicate ---
    seen: Set[Tuple[int, ...]] = set()
    unique: List[List[int]] = []
    for tape in tapes:
        key = tuple(tape)
        if key not in seen and len(tape) >= 2:
            seen.add(key)
            unique.append(tape)

    return unique
