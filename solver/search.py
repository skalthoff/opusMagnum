"""Search-based solver: Z3 layout constraints + genetic tape optimization + omsim oracle.

Architecture:
  1. Z3 generates valid layouts (from layout_z3.py)
  2. Branch-and-bound prunes by sum4 lower bound
  3. For each layout, GA optimizes tapes (from tape_ga.py)
  4. omsim via ctypes verifies every candidate (~2000/sec)
  5. Best solution survives across all layouts
"""
from __future__ import annotations
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import itertools

from .hex import HexCoord, DIRECTIONS, ORIGIN, hex_spiral
from .puzzle import Puzzle, PuzzleIO, parse_puzzle
from .solution import Solution, Part, Inst, solution_to_bytes, write_solution, PART_COSTS
from .recipe import PuzzleAnalysis, analyze_puzzle, REACTION_GLYPHS
from .simulator import Simulator, VerifyResult
from .layout_z3 import generate_layouts, compute_lower_bound, Layout, LayoutConfig
from .tape_ga import TapeGA, GAConfig, generate_geometric_tapes, Individual
from .pattern_db import PatternDB
from .glyph_model import get_glyph_spec, local_to_world


@dataclass
class SearchResult:
    solution: Solution
    metrics: dict
    score: float


def verify_solution(sol: Solution, puzzle_path: str,
                    simulator: Optional[Simulator] = None) -> Optional[dict]:
    """Verify with omsim, return metrics or None.

    Uses the Simulator (ctypes) if provided, otherwise falls back to
    reading puzzle bytes and creating a temporary simulator instance.
    """
    try:
        puzzle_bytes = Path(puzzle_path).read_bytes()
        sol_bytes = solution_to_bytes(sol)

        if simulator is None:
            simulator = Simulator()

        result: VerifyResult = simulator.verify_bytes(puzzle_bytes, sol_bytes)
        if result.valid:
            metrics = {
                'cost': result.cost,
                'cycles': result.cycles,
                'area': result.area,
                'instructions': result.instructions,
            }
            metrics['sum4'] = sum(metrics[k] for k in ('cost', 'cycles', 'area', 'instructions'))
            return metrics
    except Exception:
        pass
    return None


def search_solve(puzzle: Puzzle, puzzle_path: str,
                 target: str = 'sum4',
                 time_limit: float = 300.0,
                 verbose: bool = False,
                 pattern_db: Optional[PatternDB] = None,
                 simulator: Optional[Simulator] = None) -> Optional[SearchResult]:
    """Main solver: Z3 layouts + GA tape optimization + omsim verification."""
    t0 = time.time()

    # --- 1. Analyze puzzle ---
    analysis = analyze_puzzle(puzzle)

    glyphs_needed = []
    if analysis.recipe:
        for reaction, count in analysis.recipe.reactions.items():
            if count > 0:
                for glyph_name in REACTION_GLYPHS[reaction]:
                    glyphs_needed.append(glyph_name)

    need_bonder = analysis.needs_bonding
    n_inputs = len(puzzle.inputs)
    n_outputs = len(puzzle.outputs)

    # --- Input deduplication ---
    # When multiple inputs provide the same element type, a single input
    # station can serve for all of them.  Build a deduplicated input list
    # and a modified puzzle that the layout generators can use.
    deduped_puzzle = None
    deduped_n_inputs = n_inputs
    if all(pio.molecule.is_monoatomic for pio in puzzle.inputs):
        unique_input_types: dict = {}  # element -> first PuzzleIO index
        deduped_inputs: list = []
        for i, pio in enumerate(puzzle.inputs):
            elem = pio.molecule.atoms[0].atom_type
            if elem not in unique_input_types:
                unique_input_types[elem] = i
                deduped_inputs.append(pio)
        deduped_n_inputs = len(deduped_inputs)
        if deduped_n_inputs < n_inputs:
            # Create a modified puzzle with only unique input stations
            from copy import deepcopy
            deduped_puzzle = Puzzle(
                name=puzzle.name,
                display_name=puzzle.display_name,
                inputs=[PuzzleIO(molecule=deduped_inputs[j].molecule, index=j)
                        for j in range(deduped_n_inputs)],
                outputs=deepcopy(puzzle.outputs),
                output_scale=puzzle.output_scale,
                parts_available=puzzle.parts_available,
                is_production=puzzle.is_production,
            )

    if verbose:
        print(f'  Puzzle: {puzzle.name}')
        print(f'  Complexity: {analysis.complexity}')
        print(f'  Inputs: {n_inputs}, Outputs: {n_outputs}')
        if deduped_puzzle:
            print(f'  Deduplicated inputs: {deduped_n_inputs} (from {n_inputs})')
        print(f'  Glyphs needed: {glyphs_needed}')
        print(f'  Needs bonder: {need_bonder}')

    # --- 2. Load puzzle bytes ---
    puzzle_bytes = Path(puzzle_path).read_bytes()

    # --- 3. Initialize simulator ---
    if simulator is None:
        try:
            simulator = Simulator()
        except Exception as e:
            if verbose:
                print(f'  WARNING: Could not initialize simulator: {e}')
            return None

    # --- 4. Initialize pattern DB ---
    archive_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               'tools', 'om-archive')
    if pattern_db is None:
        pattern_db = PatternDB()
        if os.path.isdir(archive_dir):
            if verbose:
                print(f'  Scanning archive for tape patterns...')
            n_patterns = pattern_db.scan_archive(archive_dir)
            if verbose:
                print(f'  Loaded {n_patterns} tape patterns from archive')

    best: Optional[SearchResult] = None
    total_verified = 0

    # --- Phase 0: Zero-arm overlap ---
    if verbose:
        print(f'  Phase 0: Trying zero-arm overlap...')
    za = _try_zero_arm(puzzle, analysis, puzzle_bytes, simulator,
                       glyphs_needed, verbose=verbose)
    if za:
        best = za
        if verbose:
            m = za.metrics
            print(f'  Zero-arm: {m["cost"]}g/{m["cycles"]}c/'
                  f'{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')

    # Check time
    if time.time() - t0 > time_limit:
        if verbose:
            print(f'  Time limit reached after phase 0')
        return best

    # --- Phase 1: Generate layouts ---
    # Only handle monoatomic inputs for now
    if not all(pio.molecule.is_monoatomic for pio in puzzle.inputs):
        if verbose:
            print(f'  Skipping layout search: non-monoatomic inputs')
        return best

    if verbose:
        print(f'  Phase 1: Generating layouts via Z3...')

    # Generate layouts for each arm length separately to ensure diversity
    layouts = []
    for arm_len in [1, 2]:
        config = LayoutConfig(
            min_arm_len=arm_len,
            max_arm_len=arm_len,
            max_layouts=200,
        )
        if best is not None:
            config.cost_bound = best.metrics.get('cost', None)
        batch = generate_layouts(puzzle, analysis, glyphs_needed, need_bonder, config)
        layouts.extend(batch)
        if verbose:
            print(f'  Arm length {arm_len}: {len(batch)} CW-sweep layouts')

    # Generate stacked layouts separately (parts share same hex)
    from .layout_z3 import generate_stacked_layouts
    for arm_len in [1, 2]:
        config = LayoutConfig(
            min_arm_len=arm_len,
            max_arm_len=arm_len,
            max_layouts=200,
        )
        if best is not None:
            config.cost_bound = best.metrics.get('cost', None)
        stacked = generate_stacked_layouts(
            puzzle, analysis, glyphs_needed, need_bonder, config)
        layouts.extend(stacked)
        if verbose:
            print(f'  Arm length {arm_len}: {len(stacked)} stacked layouts')

    # Generate deduplicated layouts when inputs share element types
    # (e.g., P008 has 3 Fire inputs — one input station suffices)
    if deduped_puzzle is not None:
        deduped_analysis = analyze_puzzle(deduped_puzzle)
        for arm_len in [1, 2]:
            config = LayoutConfig(
                min_arm_len=arm_len,
                max_arm_len=arm_len,
                max_layouts=200,
            )
            if best is not None:
                config.cost_bound = best.metrics.get('cost', None)
            batch = generate_layouts(
                deduped_puzzle, deduped_analysis, glyphs_needed, need_bonder, config)
            layouts.extend(batch)
            if verbose:
                print(f'  Arm length {arm_len}: {len(batch)} deduped CW-sweep layouts')
            stacked = generate_stacked_layouts(
                deduped_puzzle, deduped_analysis, glyphs_needed, need_bonder, config)
            layouts.extend(stacked)
            if verbose:
                print(f'  Arm length {arm_len}: {len(stacked)} deduped stacked layouts')

    if verbose:
        print(f'  Total: {len(layouts)} candidate layouts')

    if not layouts:
        if verbose:
            print(f'  No valid layouts found')
        return best

    # --- Phase 2: Compute lower bounds and create priority queue ---
    layout_bounds = []
    for i, layout in enumerate(layouts):
        lb = compute_lower_bound(layout, analysis)
        layout_bounds.append((lb, i, layout))

    # Sort by lower bound (ascending)
    layout_bounds.sort(key=lambda x: x[0])

    if verbose:
        print(f'  Lower bounds range: {layout_bounds[0][0]} - {layout_bounds[-1][0]}')

    # --- Phase 3: For each layout, optimize tapes via GA ---
    if verbose:
        print(f'  Phase 3: GA tape optimization...')

    # Get instruction weights from pattern DB
    inst_weights = pattern_db.instruction_weights() if pattern_db.patterns else None

    for rank, (lb, layout_idx, layout) in enumerate(layout_bounds):
        # 3a. Branch-and-bound: skip if lower bound >= current best
        if best is not None and lb >= best.score:
            if verbose and rank < 5:
                print(f'  Layout {rank}: lb={lb} >= best={best.score:.0f}, pruned')
            continue

        # Check time budget
        elapsed = time.time() - t0
        if elapsed > time_limit:
            if verbose:
                print(f'  Time limit reached after {rank} layouts ({elapsed:.1f}s)')
            break

        # 3b. Build base solution (without arm)
        base_sol = layout.to_solution(puzzle, n_outputs)

        # 3c. Generate seed tapes from multiple sources
        seed_tapes = _build_seed_tapes(layout, n_inputs, pattern_db, glyphs_needed,
                                       analysis=analysis, puzzle=puzzle)

        if verbose and rank < 10:
            print(f'  Layout {rank}: cost={layout.cost}g, lb={lb}, '
                  f'{len(seed_tapes)} seed tapes')

        # 3d. Quick screening: try seed tapes directly before full GA
        layout_info = {
            'arm_pos': layout.arm_pos,
            'arm_len': layout.arm_len,
            'arm_rot': layout.arm_rot,
            'arm_type': layout.arm_type,
        }

        found_via_screen = False
        screen_cycle_limit = 1000  # valid solutions complete in <100 cycles
        for tape in seed_tapes:
            total_verified += 1
            screen_sol = layout.add_arm_with_tape(base_sol, tape)
            screen_bytes = solution_to_bytes(screen_sol)
            screen_result = simulator.verify_bytes(puzzle_bytes, screen_bytes,
                                                   cycle_limit=screen_cycle_limit)
            if screen_result.valid:
                metrics = {
                    'cost': screen_result.cost,
                    'cycles': screen_result.cycles,
                    'area': screen_result.area,
                    'instructions': screen_result.instructions,
                }
                metrics['sum4'] = sum(metrics[k] for k in ('cost', 'cycles', 'area', 'instructions'))
                score = float(metrics[target]) if target in metrics else float(metrics['sum4'])
                if best is None or score < best.score:
                    best = SearchResult(screen_sol, metrics, score)
                    found_via_screen = True
                    if verbose:
                        m = metrics
                        print(f'  ** New best (layout {rank} screen): '
                              f'{m["cost"]}g/{m["cycles"]}c/'
                              f'{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')

        if found_via_screen:
            continue  # Skip full GA for this layout, seed tape was enough

        # 3e. Run GA
        # Adjust GA config based on rank: more effort for promising layouts
        ga_config = GAConfig(
            pop_size=20 if rank < 10 else 15,
            max_generations=60 if rank < 5 else 30,
            stagnation_limit=15,
        )

        current_best_score = best.score if best is not None else None
        ga = TapeGA(simulator, ga_config, inst_weights, seed=42 + rank)
        ga_result = ga.optimize(
            base_sol, layout_info, puzzle_bytes,
            seed_tapes, target, current_best_score
        )
        total_verified += ga.total_evaluations

        # 3e. Update best if GA found a valid improvement
        if ga_result is not None and ga_result.valid:
            if best is None or ga_result.fitness < best.score:
                # Reconstruct the full solution
                final_sol = layout.add_arm_with_tape(base_sol, ga_result.tape)
                best = SearchResult(
                    solution=final_sol,
                    metrics=ga_result.metrics,
                    score=ga_result.fitness,
                )
                if verbose:
                    m = ga_result.metrics
                    print(f'  ** New best (layout {rank}): '
                          f'{m["cost"]}g/{m["cycles"]}c/'
                          f'{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')

        # 3f. Early termination if at theoretical minimum
        if best is not None:
            theory_cost = 20  # arm1
            if analysis.recipe:
                theory_cost += analysis.recipe.glyph_cost
            if need_bonder:
                theory_cost += 10
            # Sum4 minimum: cost + 1 cycle + 1 area + 1 instruction
            theory_min = theory_cost + 3
            if best.score <= theory_min:
                if verbose:
                    print(f'  Reached theoretical minimum ({theory_min}), stopping')
                break

    elapsed = time.time() - t0
    if verbose:
        print(f'  Total verified: {total_verified} in {elapsed:.1f}s')
        if best:
            m = best.metrics
            print(f'  Best: {m["cost"]}g/{m["cycles"]}c/'
                  f'{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')
        else:
            print(f'  No valid solution found')

    return best


def _build_seed_tapes(layout: Layout, n_inputs: int,
                      pattern_db: PatternDB,
                      glyphs_needed: List[str],
                      analysis: Optional[PuzzleAnalysis] = None,
                      puzzle: Optional[Puzzle] = None) -> List[List[int]]:
    """Build seed tapes for GA from multiple sources.

    Sources (priority order):
      1. Compiled tapes from dataflow analysis (highest priority)
      2. Geometric templates based on layout geometry
      3. Similar tapes from archive pattern DB
      4. Common tape templates from archive
    """
    seed_tapes: List[List[int]] = []
    n_stations = len(layout.stations)

    # Source 1: Compiled tapes (dataflow-derived, highest priority)
    if analysis is not None and puzzle is not None:
        from .tape_compiler import compile_tapes
        compiled = compile_tapes(layout, analysis, puzzle)
        seed_tapes.extend(compiled)

    # Source 2: Geometric templates
    geo_tapes = generate_geometric_tapes(n_stations, n_inputs, layout.directions)
    seed_tapes.extend(geo_tapes)

    # Source 2: Archive similar tapes (25%)
    if pattern_db.patterns:
        n_glyphs = len(glyphs_needed)
        similar = pattern_db.get_similar_tapes(
            n_arms=1,
            n_glyphs_range=(max(0, n_glyphs - 1), n_glyphs + 2),
            limit=15,
        )
        for pat in similar:
            seed_tapes.append(list(pat.tape))

    # Source 3: Common templates from archive (15%)
    if pattern_db.patterns:
        common = pattern_db.common_tape_templates(n_arms=1, limit=8)
        for tape_tuple in common:
            seed_tapes.append(list(tape_tuple))

    # Deduplicate
    seen = set()
    unique = []
    for tape in seed_tapes:
        key = tuple(tape)
        if key not in seen:
            seen.add(key)
            unique.append(tape)

    return unique


# =============================================================================
# ZERO-ARM OVERLAP
# =============================================================================

def _make_metrics(result: VerifyResult) -> dict:
    """Build a metrics dict (with sum4) from a valid VerifyResult."""
    metrics = {
        'cost': result.cost,
        'cycles': result.cycles,
        'area': result.area,
        'instructions': result.instructions,
    }
    metrics['sum4'] = sum(metrics[k] for k in ('cost', 'cycles', 'area', 'instructions'))
    return metrics


def _try_zero_arm(puzzle: Puzzle, analysis: PuzzleAnalysis,
                  puzzle_bytes: bytes, simulator: Simulator,
                  glyphs_needed: List[str],
                  verbose: bool = False,
                  time_limit: float = 15.0) -> Optional[SearchResult]:
    """Try to solve with zero arms by overlapping inputs/outputs on glyphs.

    Uses a glyph-guided search: for each glyph placement (position + rotation),
    compute slot world positions, then try placing inputs at those slots.
    Any glyph type can participate (projection, purification, etc.).

    Also tries a no-glyph bonding-only path for puzzles where the output
    is just the inputs bonded together.

    Exploits translation/rotation symmetry of the infinite board to reduce
    the search space (fixing glyph position to ORIGIN and glyph rotation to 0).
    """
    # All inputs must be monoatomic for zero-arm overlap
    if not all(pio.molecule.is_monoatomic for pio in puzzle.inputs):
        return None
    # Must have at least one output
    if len(puzzle.outputs) < 1:
        return None

    t0 = time.time()
    n_inputs = len(puzzle.inputs)
    best: Optional[SearchResult] = None
    n_checked = 0

    # Monoatomic output rotation invariance: rotating a single atom is identity
    all_mono_out = all(len(pio.molecule.atoms) <= 1 for pio in puzzle.outputs)
    out_rotations = [0] if all_mono_out else range(6)

    # Compute theoretical minimum sum4 for early exit:
    # cost of glyphs + (bonder if needed) + 0 arms + minimum 2 cycles + 1 area + 0 instructions
    theory_cost = sum(PART_COSTS.get(g, 0) for g in glyphs_needed)
    if analysis.needs_bonding:
        theory_cost += 10  # bonder
    # Minimum sum4: cost + 1cycle + 1area + 0instructions (absolute floor)
    theory_min_sum4 = theory_cost + 2

    def _check_and_update(sol: Solution) -> bool:
        """Verify a candidate solution and update best. Returns True for early exit."""
        nonlocal best, n_checked
        n_checked += 1
        # Time cap check every 500 candidates
        if n_checked % 500 == 0 and time.time() - t0 > time_limit:
            if verbose:
                print(f'  Zero-arm time cap ({time_limit}s) after {n_checked} candidates')
            return True
        sol_bytes = solution_to_bytes(sol)
        result = simulator.verify_bytes(puzzle_bytes, sol_bytes)
        if result.valid:
            metrics = _make_metrics(result)
            s4 = metrics['sum4']
            if best is None or s4 < best.score:
                best = SearchResult(sol, metrics, s4)
                if s4 <= theory_min_sum4:
                    return True  # At theoretical minimum, early exit
        return False

    # --- Path 1: Glyph-guided search ---
    # For each glyph needed, try all placements and map inputs to slot positions.
    # When bonding is needed, bonder slot positions are also candidates for inputs.
    bonder_spec = None
    if analysis.needs_bonding:
        try:
            bonder_spec = get_glyph_spec('bonder')
        except KeyError:
            pass

    for glyph_name in glyphs_needed:
        try:
            spec = get_glyph_spec(glyph_name)
        except KeyError:
            continue

        input_active_slots = [s for s in spec.slots if s.role in ('input', 'active')]
        output_slots = [s for s in spec.slots if s.role == 'output']

        for glyph_pos in [ORIGIN]:
            for glyph_rot in [0]:
                ia_world = [local_to_world(glyph_pos, glyph_rot, s.du, s.dv)
                            for s in input_active_slots]
                out_world = [local_to_world(glyph_pos, glyph_rot, s.du, s.dv)
                             for s in output_slots]

                if analysis.needs_bonding and bonder_spec:
                    # Iterate bonder rotations to include bonder slots as candidates
                    bonder_rots = range(6)
                else:
                    bonder_rots = [None]

                for brot in bonder_rots:
                    # Build candidate positions from glyph slots + bonder slots
                    candidates_raw = list(ia_world) + [glyph_pos]
                    if brot is not None and bonder_spec:
                        for s in bonder_spec.slots:
                            candidates_raw.append(
                                local_to_world(glyph_pos, brot, s.du, s.dv))

                    # Deduplicate
                    seen_pos = set()
                    candidate_positions = []
                    for p in candidates_raw:
                        if p not in seen_pos:
                            seen_pos.add(p)
                            candidate_positions.append(p)

                    for input_assignment in itertools.product(
                            candidate_positions, repeat=n_inputs):
                        input_parts = [
                            Part(name='input', position=input_assignment[i],
                                 io_index=i)
                            for i in range(n_inputs)
                        ]
                        glyph_part = Part(name=glyph_name, position=glyph_pos,
                                          rotation=glyph_rot)

                        out_candidates = list(
                            set(input_assignment) | set(out_world) | {glyph_pos})

                        for out_pos in out_candidates:
                            for out_rot in out_rotations:
                                base_parts = input_parts + [glyph_part]

                                if brot is not None:
                                    sol = Solution(
                                        puzzle_name=puzzle.name,
                                        solution_name="ZA")
                                    sol.parts = list(base_parts) + [
                                        Part(name='bonder',
                                             position=glyph_pos,
                                             rotation=brot),
                                        Part(name='out-std',
                                             position=out_pos,
                                             rotation=out_rot,
                                             io_index=0),
                                    ]
                                    if _check_and_update(sol):
                                        if verbose:
                                            print(f'  Zero-arm checked '
                                                  f'{n_checked} candidates')
                                        return best
                                else:
                                    sol = Solution(
                                        puzzle_name=puzzle.name,
                                        solution_name="ZA")
                                    sol.parts = list(base_parts) + [
                                        Part(name='out-std',
                                             position=out_pos,
                                             rotation=out_rot,
                                             io_index=0),
                                    ]
                                    if _check_and_update(sol):
                                        if verbose:
                                            print(f'  Zero-arm checked '
                                                  f'{n_checked} candidates')
                                        return best

    # --- Path 2: No-glyph bonding-only path ---
    # For puzzles where the output is just the inputs bonded together
    # (no transmutation glyphs needed, but bonding is required)
    if not glyphs_needed and analysis.needs_bonding:
        for bonder_pos in [ORIGIN]:
            for brot in range(6):
                # Compute bonder slot world positions
                try:
                    bonder_spec = get_glyph_spec('bonder')
                except KeyError:
                    break
                bonder_slots_world = [
                    local_to_world(bonder_pos, brot, s.du, s.dv)
                    for s in bonder_spec.slots
                ]
                candidate_positions = list(set(bonder_slots_world + [bonder_pos]))

                if len(candidate_positions) < n_inputs:
                    continue

                for input_assignment in itertools.permutations(candidate_positions, n_inputs):
                    input_parts = [
                        Part(name='input', position=input_assignment[i], io_index=i)
                        for i in range(n_inputs)
                    ]
                    bonder_part = Part(name='bonder', position=bonder_pos,
                                       rotation=brot)

                    out_candidates = list(set(input_assignment) | set(bonder_slots_world))

                    for out_idx in range(len(puzzle.outputs)):
                        for out_pos in out_candidates:
                            for out_rot in out_rotations:
                                sol = Solution(puzzle_name=puzzle.name,
                                               solution_name="ZA")
                                sol.parts = input_parts + [
                                    bonder_part,
                                    Part(name='out-std', position=out_pos,
                                         rotation=out_rot, io_index=out_idx),
                                ]
                                if _check_and_update(sol):
                                    if verbose:
                                        print(f'  Zero-arm checked {n_checked} candidates')
                                    return best

    # --- Path 3: Trivial (no glyphs, no bonding) ---
    # Output = single input atom, just overlap input and output
    if not glyphs_needed and not analysis.needs_bonding:
        for pos in [ORIGIN]:
            for io_idx in range(n_inputs):
                for out_idx in range(len(puzzle.outputs)):
                    for out_rot in out_rotations:
                        sol = Solution(puzzle_name=puzzle.name, solution_name="ZA")
                        sol.parts = [
                            Part(name='input', position=pos, io_index=io_idx),
                            Part(name='out-std', position=pos, rotation=out_rot,
                                 io_index=out_idx),
                        ]
                        if _check_and_update(sol):
                            if verbose:
                                print(f'  Zero-arm checked {n_checked} candidates')
                            return best

    if verbose:
        print(f'  Zero-arm checked {n_checked} candidates')

    return best


# =============================================================================
# BATCH SOLVING
# =============================================================================

def search_all_puzzles(puzzle_dir: str, target: str = 'sum4',
                       time_limit: float = 60.0,
                       verbose: bool = True) -> Dict[str, SearchResult]:
    """Run solver on all puzzles in a directory.

    Reuses the Simulator and PatternDB across puzzles for efficiency.
    """
    results: Dict[str, SearchResult] = {}

    # Initialize shared resources once
    try:
        simulator = Simulator()
    except Exception as e:
        if verbose:
            print(f'ERROR: Could not initialize simulator: {e}')
        return results

    archive_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               'tools', 'om-archive')
    pattern_db = PatternDB()
    if os.path.isdir(archive_dir):
        if verbose:
            print(f'Scanning archive for tape patterns...')
        n_patterns = pattern_db.scan_archive(archive_dir)
        if verbose:
            print(f'Loaded {n_patterns} patterns')

    # Find all puzzle files
    puzzles = []
    for root, dirs, files in os.walk(puzzle_dir):
        for f in files:
            if f.endswith('.puzzle'):
                puzzles.append((f.replace('.puzzle', ''), os.path.join(root, f)))
    puzzles.sort()

    if verbose:
        print(f'\nFound {len(puzzles)} puzzles\n')

    for pid, ppath in puzzles:
        try:
            p = parse_puzzle(ppath)
            if verbose:
                print(f'\n{"="*60}')
                print(f'{pid}: {p.name}')
                print(f'{"="*60}')
            result = search_solve(
                p, ppath,
                target=target,
                time_limit=time_limit,
                verbose=verbose,
                pattern_db=pattern_db,
                simulator=simulator,
            )
            if result:
                results[pid] = result
                m = result.metrics
                if verbose:
                    print(f'  => {m["cost"]}g/{m["cycles"]}c/'
                          f'{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')
            else:
                if verbose:
                    print(f'  => no solution')
        except Exception as e:
            if verbose:
                print(f'  => ERROR: {e}')

    if verbose:
        print(f'\n{"="*60}')
        print(f'Summary: {len(results)}/{len(puzzles)} puzzles solved')

    return results
