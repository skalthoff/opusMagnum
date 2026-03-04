"""Search-based solver: Z3 layout constraints + genetic tape optimization + omsim oracle.

Architecture:
  1. Z3 generates valid layouts (from layout_z3.py)
  2. Branch-and-bound prunes by sum4 lower bound
  3. For each layout, GA optimizes tapes (from tape_ga.py)
  4. omsim via ctypes verifies every candidate
  5. Best solution survives across all layouts
"""
from __future__ import annotations
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import itertools

from .hex import HexCoord, DIRECTIONS, ORIGIN, hex_spiral
from .puzzle import Puzzle, PuzzleIO, parse_puzzle
from .recipe import PuzzleAnalysis, analyze_puzzle, REACTION_GLYPHS
from .production_planner import generate_plans, ProductionPlan
from .simulator import Simulator, VerifyResult, PuzzleContext
from .layout_z3 import (generate_layouts, compute_lower_bound, Layout,
                        LayoutConfig, generate_layouts_from_graph,
                        _find_glyph_placements,
                        ArmSpec, MultiArmLayout, generate_multi_arm_layouts,
                        extract_layout_from_solution)
from .solution import (Solution, Part, Inst, solution_to_bytes, write_solution,
                       PART_COSTS, parse_solution as parse_solution_file,
                       CachedSolutionBase, CachedMultiArmSolutionBase)
from .tape_ga import (TapeGA, GAConfig, generate_geometric_tapes, Individual,
                      _is_obviously_invalid, MultiTapeGA, MultiArmIndividual)
from .pattern_db import PatternDB
from .glyph_model import get_glyph_spec, local_to_world
from .station_graph import build_station_graph, StationGraph, graph_to_plan


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


def _ga_worker(args):
    """Worker process: run GA on a single layout.

    Returns (rank, best_tape, metrics, score, n_evals).
    best_tape is None if no valid solution was found.
    """
    (rank, base_sol, layout_info, puzzle_bytes, seed_tapes,
     target, current_best_score, inst_weights, ga_seed) = args

    sim = Simulator()
    ga_config = GAConfig(
        pop_size=20 if rank < 10 else 15,
        max_generations=60 if rank < 5 else 30,
        stagnation_limit=15,
    )

    ga = TapeGA(sim, ga_config, inst_weights, seed=ga_seed)
    ga_result = ga.optimize(
        base_sol, layout_info, puzzle_bytes,
        seed_tapes, target, current_best_score
    )

    n_evals = ga.total_evaluations
    if ga_result is not None and ga_result.valid:
        return (rank, ga_result.tape, ga_result.metrics, ga_result.fitness, n_evals)
    return (rank, None, None, None, n_evals)


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

    plans = generate_plans(puzzle, analysis)

    # Use first plan's glyphs for zero-arm and initial display
    glyphs_needed = plans[0].glyph_names if plans else []
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
        print(f'  Plans: {len(plans)}')
        for pi, plan in enumerate(plans):
            print(f'    Plan {pi}: glyphs={plan.glyph_names}, '
                  f'grabs={plan.total_grabs}, cost~{plan.estimated_cost}')
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
    # Cap zero-arm time: simple puzzles get 5s, complex ones get 2s
    za_time = 2.0 if n_inputs >= 3 or (analysis.needs_bonding and n_inputs >= 2) else 5.0
    za = _try_zero_arm(puzzle, analysis, puzzle_bytes, simulator,
                       glyphs_needed, verbose=verbose, time_limit=za_time)
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

    # --- Phase 0b: Self-return layouts ---
    # For puzzles where the arm can grab from input, sweep through glyph(s),
    # and RESET to deposit back at the same position (which is also the output).
    # The P013 WR uses this: input=output position, arm sweeps through calcification.
    if verbose:
        print(f'  Phase 0b: Trying self-return layouts...')
    sr = _try_self_return_layouts(
        puzzle, analysis, puzzle_bytes, simulator,
        plans, pattern_db, target, verbose=verbose,
        time_limit=min(10.0, max(0, time_limit - (time.time() - t0))),
        current_best=best)
    if sr is not None and (best is None or sr.score < best.score):
        best = sr
        if verbose:
            m = sr.metrics
            print(f'  Self-return: {m["cost"]}g/{m["cycles"]}c/'
                  f'{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')

    # Check time
    if time.time() - t0 > time_limit:
        if verbose:
            print(f'  Time limit reached after phase 0b')
        return best

    # --- Phase 1: Generate layouts ---
    has_mono_inputs = all(pio.molecule.is_monoatomic for pio in puzzle.inputs)
    if not has_mono_inputs:
        if verbose:
            print(f'  Non-monoatomic inputs: skipping CW/stacked layouts, trying graph-constrained only')

    if verbose:
        print(f'  Phase 1: Generating layouts via Z3...')

    # Generate layouts for each plan variant
    from .layout_z3 import generate_stacked_layouts
    # Each entry: (layout, plan, optional_graph)
    layouts_with_plans: List[Tuple[Layout, ProductionPlan, Optional[StationGraph]]] = []

    # CW-sweep and stacked layouts assume monoatomic inputs — skip for polyatomic
    if has_mono_inputs:
        for plan in plans:
            plan_glyphs = plan.glyph_names
            plan_bonder = plan.need_bonder
            plan_bonder_name = plan.bonder_type

            # Generate layouts for each arm length separately to ensure diversity
            for arm_len in [1, 2, 3]:
                config = LayoutConfig(
                    min_arm_len=arm_len,
                    max_arm_len=arm_len,
                    max_layouts=200,
                )
                if best is not None:
                    config.cost_bound = best.metrics.get('cost', None)
                batch = generate_layouts(puzzle, analysis, plan_glyphs,
                                         plan_bonder, config,
                                         bonder_name=plan_bonder_name)
                for lay in batch:
                    layouts_with_plans.append((lay, plan, None))
                if verbose:
                    print(f'  Plan glyphs={plan_glyphs} bonder={plan_bonder_name}: '
                          f'arm{arm_len}: {len(batch)} CW-sweep layouts')

            # Generate stacked layouts separately (parts share same hex)
            for arm_len in [1, 2, 3]:
                config = LayoutConfig(
                    min_arm_len=arm_len,
                    max_arm_len=arm_len,
                    max_layouts=200,
                )
                if best is not None:
                    config.cost_bound = best.metrics.get('cost', None)
                stacked = generate_stacked_layouts(
                    puzzle, analysis, plan_glyphs, plan_bonder, config,
                    bonder_name=plan_bonder_name)
                for lay in stacked:
                    layouts_with_plans.append((lay, plan, None))
                if verbose:
                    print(f'  Plan glyphs={plan_glyphs} bonder={plan_bonder_name}: '
                          f'arm{arm_len}: {len(stacked)} stacked layouts')

            # Generate deduplicated layouts when inputs share element types
            if deduped_puzzle is not None:
                deduped_analysis = analyze_puzzle(deduped_puzzle)
                for arm_len in [1, 2, 3]:
                    config = LayoutConfig(
                        min_arm_len=arm_len,
                        max_arm_len=arm_len,
                        max_layouts=200,
                    )
                    if best is not None:
                        config.cost_bound = best.metrics.get('cost', None)
                    batch = generate_layouts(
                        deduped_puzzle, deduped_analysis, plan_glyphs,
                        plan_bonder, config, bonder_name=plan_bonder_name)
                    for lay in batch:
                        layouts_with_plans.append((lay, plan, None))
                    if verbose:
                        print(f'  Plan glyphs={plan_glyphs} bonder={plan_bonder_name}: '
                              f'arm{arm_len}: {len(batch)} deduped CW-sweep layouts')
                    stacked = generate_stacked_layouts(
                        deduped_puzzle, deduped_analysis, plan_glyphs,
                        plan_bonder, config, bonder_name=plan_bonder_name)
                    for lay in stacked:
                        layouts_with_plans.append((lay, plan, None))
                    if verbose:
                        print(f'  Plan glyphs={plan_glyphs} bonder={plan_bonder_name}: '
                              f'arm{arm_len}: {len(stacked)} deduped stacked layouts')

    # --- Phase 1b: Station graph constrained layouts ---
    # Build station graphs and generate alignment-constrained layouts
    graphs = build_station_graph(puzzle, analysis)
    graph_plans: Dict[int, ProductionPlan] = {}  # graph_idx -> plan

    if verbose and graphs:
        print(f'  Station graphs: {len(graphs)} variants')

    for gi, graph in enumerate(graphs):
        # Convert graph to plan for tape compilation compatibility
        plan = graph_to_plan(graph, puzzle, analysis)
        graph_plans[gi] = plan

        for arm_len in [1, 2, 3]:
            config = LayoutConfig(
                min_arm_len=arm_len,
                max_arm_len=arm_len,
                max_layouts=200,
            )
            if best is not None:
                config.cost_bound = best.metrics.get('cost', None)

            graph_layouts = generate_layouts_from_graph(
                graph, puzzle, analysis, config)

            for lay in graph_layouts:
                layouts_with_plans.append((lay, plan, graph))

            if verbose and graph_layouts:
                print(f'  Graph {gi} arm{arm_len}: {len(graph_layouts)} '
                      f'constrained layouts (bonder={graph.bonder_type})')

        # Also try with deduped puzzle
        if deduped_puzzle is not None:
            deduped_analysis_g = analyze_puzzle(deduped_puzzle)
            deduped_graphs = build_station_graph(deduped_puzzle, deduped_analysis_g)
            for dg in deduped_graphs:
                dplan = graph_to_plan(dg, deduped_puzzle, deduped_analysis_g)
                for arm_len in [1, 2, 3]:
                    config = LayoutConfig(
                        min_arm_len=arm_len,
                        max_arm_len=arm_len,
                        max_layouts=200,
                    )
                    if best is not None:
                        config.cost_bound = best.metrics.get('cost', None)
                    dg_layouts = generate_layouts_from_graph(
                        dg, deduped_puzzle, deduped_analysis_g, config)
                    for lay in dg_layouts:
                        layouts_with_plans.append((lay, dplan, dg))
                    if verbose and dg_layouts:
                        print(f'  Deduped graph arm{arm_len}: '
                              f'{len(dg_layouts)} constrained layouts')

    if verbose:
        print(f'  Total: {len(layouts_with_plans)} candidate layouts')

    if not layouts_with_plans:
        if verbose:
            print(f'  No valid layouts found')
        return best

    # --- Phase 2: Compute lower bounds and create priority queue ---
    layout_bounds = []
    for i, (layout, plan, graph_opt) in enumerate(layouts_with_plans):
        lb = compute_lower_bound(layout, analysis)
        layout_bounds.append((lb, i, layout, plan, graph_opt))

    # Sort by lower bound (ascending)
    layout_bounds.sort(key=lambda x: x[0])

    if verbose:
        print(f'  Lower bounds range: {layout_bounds[0][0]} - {layout_bounds[-1][0]}')

    # --- Phase 3: For each layout, optimize tapes via GA ---
    if verbose:
        print(f'  Phase 3: GA tape optimization...')

    # Get instruction weights from pattern DB
    inst_weights = pattern_db.instruction_weights() if pattern_db.patterns else None

    # Create reusable puzzle context for screening (parses puzzle once)
    puzzle_ctx = simulator.create_puzzle_context(puzzle_bytes)

    # Theoretical minimum for early termination
    theory_cost = 20  # arm1
    if analysis.recipe:
        theory_cost += analysis.recipe.glyph_cost
    if need_bonder:
        theory_cost += 10
    theory_min = theory_cost + 3  # cost + 1 cycle + 1 area + 1 instruction

    # --- Phase 3a: Sequential screening (fast, provides pruning) ---
    from .solution import CachedSolutionBase
    ga_candidates = []  # (rank, layout, base_sol, layout_info, seed_tapes, plan)

    for rank, (lb, layout_idx, layout, plan, graph_opt) in enumerate(layout_bounds):
        # Branch-and-bound: skip if lower bound >= current best
        if best is not None and lb >= best.score:
            continue

        # Check time budget
        if time.time() - t0 > time_limit:
            if verbose:
                print(f'  Time limit reached during screening after {rank} layouts')
            break

        # Build base solution (without arm)
        base_sol = layout.to_solution(puzzle, n_outputs)

        # Generate seed tapes from multiple sources
        seed_tapes = _build_seed_tapes(layout, n_inputs, pattern_db,
                                       plan.glyph_names,
                                       analysis=analysis, puzzle=puzzle,
                                       plan=plan, graph=graph_opt)

        layout_info = {
            'arm_pos': layout.arm_pos,
            'arm_len': layout.arm_len,
            'arm_rot': layout.arm_rot,
            'arm_type': layout.arm_type,
        }

        # Quick screening: try seed tapes directly
        found_via_screen = False
        screen_cache = CachedSolutionBase(base_sol, layout_info)
        for tape in seed_tapes:
            if _is_obviously_invalid(tape):
                continue
            total_verified += 1
            screen_bytes = screen_cache.splice(tape)
            screen_result = puzzle_ctx.verify(screen_bytes, cycle_limit=1000)
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
                    screen_sol = layout.add_arm_with_tape(base_sol, tape)
                    best = SearchResult(screen_sol, metrics, score)
                    found_via_screen = True
                    if verbose:
                        m = metrics
                        print(f'  ** New best (layout {rank} screen): '
                              f'{m["cost"]}g/{m["cycles"]}c/'
                              f'{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')

        # Early termination at theoretical minimum
        if best is not None and best.score <= theory_min:
            if verbose:
                print(f'  Reached theoretical minimum ({theory_min}), stopping')
            break

        if not found_via_screen:
            ga_candidates.append((rank, layout, base_sol, layout_info, seed_tapes, plan))

    puzzle_ctx.destroy()

    if verbose:
        print(f'  Screening done: {len(ga_candidates)} layouts need GA')

    # --- Phase 3b: GA on remaining layouts (parallel if possible, else sequential) ---
    if ga_candidates and (best is None or best.score > theory_min):
        # Prepare worker arguments (with pruning)
        # best_tape_so_far: warm-start subsequent layouts with the best tape found so far
        best_tape_so_far = None
        worker_args = []
        # Keep mapping from rank to (layout, base_sol) for solution reconstruction
        rank_to_layout = {}
        for rank, layout, base_sol, layout_info, seed_tapes, plan in ga_candidates:
            if best is not None:
                lb = compute_lower_bound(layout, analysis)
                if lb >= best.score:
                    continue
            if time.time() - t0 > time_limit:
                break
            current_best_score = best.score if best is not None else None
            # Warm-start: prepend best tape from any previous GA result
            effective_seeds = seed_tapes
            if best_tape_so_far is not None:
                effective_seeds = [best_tape_so_far] + seed_tapes
            worker_args.append((
                rank, base_sol, layout_info, puzzle_bytes, effective_seeds,
                target, current_best_score, inst_weights, 42 + rank
            ))
            rank_to_layout[rank] = (layout, base_sol)

        if worker_args:
            # Try parallel execution, fall back to sequential
            n_workers = min(max(1, os.cpu_count() - 1), 8, len(worker_args))
            use_parallel = n_workers > 1

            if use_parallel:
                try:
                    pool = ProcessPoolExecutor(max_workers=n_workers)
                    if verbose:
                        print(f'  Starting parallel GA with {n_workers} workers '
                              f'on {len(worker_args)} layouts...')
                except (PermissionError, OSError):
                    use_parallel = False
                    if verbose:
                        print(f'  Parallel GA unavailable, using sequential...')

            if use_parallel:
                try:
                    futures = {pool.submit(_ga_worker, args): args[0]
                               for args in worker_args}
                    for future in as_completed(futures):
                        rank_id = futures[future]
                        try:
                            rank_result, best_tape, metrics, score, n_evals = future.result()
                            total_verified += n_evals
                            if best_tape is not None and (best is None or score < best.score):
                                layout, base_sol = rank_to_layout[rank_result]
                                final_sol = layout.add_arm_with_tape(base_sol, best_tape)
                                best = SearchResult(
                                    solution=final_sol,
                                    metrics=metrics,
                                    score=score,
                                )
                                if verbose:
                                    m = metrics
                                    print(f'  ** New best (layout {rank_result} GA): '
                                          f'{m["cost"]}g/{m["cycles"]}c/'
                                          f'{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')
                        except Exception as e:
                            if verbose:
                                print(f'  GA worker for layout {rank_id} failed: {e}')
                finally:
                    pool.shutdown(wait=False)
            else:
                # Sequential fallback
                if verbose:
                    print(f'  Running GA sequentially on {len(worker_args)} layouts...')
                seq_best_tape: Optional[List[int]] = None
                # Reserve time for later phases (archive, multi-arm)
                # Short limits: reserve less; long limits: reserve more
                reserve_frac = 0.3 if time_limit > 60 else 0.15
                ga_deadline = t0 + time_limit * (1.0 - reserve_frac)
                for args in worker_args:
                    if time.time() > ga_deadline:
                        if verbose:
                            print(f'  GA time budget reached, reserving time for later phases')
                        break
                    # Warm-start: inject best tape from previous sequential result
                    if seq_best_tape is not None:
                        (r, bs, li, pb, seeds, tgt, cbs, iw, gs) = args
                        if seq_best_tape not in seeds:
                            args = (r, bs, li, pb, [seq_best_tape] + seeds,
                                    tgt, cbs, iw, gs)
                    rank_result, best_tape, metrics, score, n_evals = _ga_worker(args)
                    total_verified += n_evals
                    if best_tape is not None and (best is None or score < best.score):
                        layout, base_sol = rank_to_layout[rank_result]
                        final_sol = layout.add_arm_with_tape(base_sol, best_tape)
                        best = SearchResult(
                            solution=final_sol,
                            metrics=metrics,
                            score=score,
                        )
                        seq_best_tape = best_tape
                        if verbose:
                            m = metrics
                            print(f'  ** New best (layout {rank_result} GA): '
                                  f'{m["cost"]}g/{m["cycles"]}c/'
                                  f'{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')
                    elif best_tape is not None and seq_best_tape is None:
                        # Valid tape found but not better than best; still useful as seed
                        seq_best_tape = best_tape
                    # Update pruning for subsequent layouts
                    if best is not None and best.score <= theory_min:
                        if verbose:
                            print(f'  Reached theoretical minimum ({theory_min}), stopping')
                        break

    # --- Phase 4: Final polish (re-run GA on best layout with double budget) ---
    if (best is not None and best.score > theory_min
            and time.time() - t0 < time_limit):
        # Find the layout that produced the best result by checking all candidates
        polish_layout = None
        polish_base_sol = None
        polish_seeds = None
        polish_plan = None
        for rank, layout, base_sol, layout_info, seed_tapes, plan in ga_candidates:
            # Reconstruct and compare: the best solution came from one of these
            # Use layout matching via rank_to_layout if available
            if rank in rank_to_layout:
                lay, bs = rank_to_layout[rank]
                if lay is layout:
                    polish_layout = layout
                    polish_base_sol = base_sol
                    polish_seeds = seed_tapes
                    polish_plan = plan
                    break
        # If best came from screening (not GA), find the layout from layout_bounds
        if polish_layout is None:
            # Try to match best solution's parts to a layout
            for lb, idx, layout, plan, graph_opt in layout_bounds:
                base_sol = layout.to_solution(puzzle, n_outputs)
                polish_layout = layout
                polish_base_sol = base_sol
                polish_seeds = _build_seed_tapes(
                    layout, n_inputs, pattern_db,
                    plan.glyph_names, analysis=analysis,
                    puzzle=puzzle, plan=plan, graph=graph_opt)
                polish_plan = plan
                break  # Use the top-ranked layout as fallback

        if polish_layout is not None:
            if verbose:
                print(f'  Phase 4: Final polish on best layout (pop=40, gen=120)...')
            polish_layout_info = {
                'arm_pos': polish_layout.arm_pos,
                'arm_len': polish_layout.arm_len,
                'arm_rot': polish_layout.arm_rot,
                'arm_type': polish_layout.arm_type,
            }
            # Include the best solution's tape as a seed
            best_tape_seed = []
            if best.solution.parts:
                for p in best.solution.parts:
                    if p.is_arm and p.instructions:
                        best_tape_seed = p.get_tape(max(i.index for i in p.instructions) + 1)
                        break
            polish_effective_seeds = ([best_tape_seed] if best_tape_seed else []) + (polish_seeds or [])
            polish_args = (
                0, polish_base_sol, polish_layout_info, puzzle_bytes,
                polish_effective_seeds, target,
                best.score, inst_weights, 99999
            )
            # Override GA config for polish: double budget
            def _polish_worker(args):
                (rank, base_sol, layout_info, pb, seeds,
                 tgt, cbs, iw, gs) = args
                sim = Simulator()
                ga_config = GAConfig(
                    pop_size=40,
                    max_generations=120,
                    stagnation_limit=30,
                )
                ga = TapeGA(sim, ga_config, iw, seed=gs)
                ga_result = ga.optimize(
                    base_sol, layout_info, pb, seeds, tgt, cbs)
                n_evals = ga.total_evaluations
                if ga_result is not None and ga_result.valid:
                    return (rank, ga_result.tape, ga_result.metrics,
                            ga_result.fitness, n_evals)
                return (rank, None, None, None, n_evals)

            rank_result, best_tape, metrics, score, n_evals = _polish_worker(polish_args)
            total_verified += n_evals
            if best_tape is not None and score < best.score:
                final_sol = polish_layout.add_arm_with_tape(polish_base_sol, best_tape)
                best = SearchResult(
                    solution=final_sol,
                    metrics=metrics,
                    score=score,
                )
                if verbose:
                    m = metrics
                    print(f'  ** New best (polish GA): '
                          f'{m["cost"]}g/{m["cycles"]}c/'
                          f'{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')
            elif verbose:
                print(f'  Polish GA did not improve ({n_evals} evals)')

    # --- Phase 5a: Archive-guided search ---
    # Use archive solutions as layout templates. Especially useful for journal
    # puzzles that need multi-arm coordination.
    if time.time() - t0 < time_limit:
        archive_time = min(time_limit - (time.time() - t0), 60.0)
        if verbose:
            print(f'  Phase 5a: Archive-guided search ({archive_time:.0f}s budget)...')
        archive_result = _try_archive_guided_search(
            puzzle, puzzle_path, analysis, puzzle_bytes, simulator,
            target=target, time_limit=archive_time,
            verbose=verbose, current_best=best)
        if archive_result is not None and (best is None or archive_result.score < best.score):
            best = archive_result

    # --- Phase 5b: Multi-arm escalation ---
    # Try multi-arm solutions when single-arm failed or has room to improve.
    # Only attempt when: time remaining > 10s AND (no solution found OR
    # best single-arm score leaves room for multi-arm to win despite cost overhead).
    time_remaining = time_limit - (time.time() - t0)
    multi_arm_overhead = 20  # extra arm costs ~20g minimum
    should_try_multi = (
        time_remaining > 10
        and (best is None
             or (best.score > theory_min + multi_arm_overhead))
    )
    if should_try_multi:
        if verbose:
            print(f'  Phase 5: Multi-arm escalation ({time_remaining:.0f}s remaining)...')
        multi_result = _try_multi_arm_layouts(
            puzzle, analysis, plans, graphs,
            puzzle_bytes, simulator,
            target=target,
            time_limit=min(time_remaining, 30.0),
            verbose=verbose,
            current_best=best,
        )
        if multi_result is not None and (best is None or multi_result.score < best.score):
            best = multi_result

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


def _try_self_return_layouts(
    puzzle: Puzzle, analysis: PuzzleAnalysis,
    puzzle_bytes: bytes, simulator: Simulator,
    plans: List[ProductionPlan],
    pattern_db: PatternDB,
    target: str = 'sum4',
    verbose: bool = False,
    time_limit: float = 5.0,
    current_best: Optional[SearchResult] = None,
) -> Optional[SearchResult]:
    """Try self-return layouts where input and output share the same position.

    The arm grabs from input, sweeps through glyph(s) (which fire on the held
    atom as it passes through), and RESET returns the arm to its start position.
    The processed atom is deposited at the arm tip on reset, which is also the
    output position.

    This is the pattern used by the P013 WR: GRAB, CCW, CCW, CW, RESET.

    Strategy: fix arm at ORIGIN, compute sweep tip positions. Place glyphs and
    bonders at positions where their slots overlap the sweep arc.
    """
    if not all(pio.molecule.is_monoatomic for pio in puzzle.inputs):
        return None
    if not plans:
        return None

    t0 = time.time()
    best: Optional[SearchResult] = current_best
    n_checked = 0

    puzzle_ctx = simulator.create_puzzle_context(puzzle_bytes)
    from .solution import CachedSolutionBase

    all_mono_out = all(len(pio.molecule.atoms) <= 1 for pio in puzzle.outputs)
    out_rots = [0] if all_mono_out else list(range(6))
    pass_tapes = _generate_pass_through_tapes_compact()
    arm_pos = ORIGIN

    # Build all (plan, arm_len) configs, interleaved by arm_len for diversity
    configs = [(plan, arm_len) for arm_len in [1, 2] for plan in plans]
    per_config_budget = time_limit / max(len(configs), 1)

    for cfg_idx, (plan, arm_len) in enumerate(configs):
        if time.time() - t0 > time_limit:
            break
        config_deadline = t0 + per_config_budget * (cfg_idx + 1)
        glyph_names = plan.glyph_names
        need_bonder = plan.need_bonder
        bonder_name = plan.bonder_type or 'bonder-speed'

        # Sweep tip positions (same for all arm_rot values)
        sweep_tips = [HexCoord(DIRECTIONS[d].q * arm_len,
                               DIRECTIONS[d].r * arm_len) for d in range(6)]
        sweep_set = set(sweep_tips) | {arm_pos}

        # Glyph placements: slot must overlap a sweep position
        glyph_options = []
        for gname in glyph_names:
            try:
                spec = get_glyph_spec(gname)
            except KeyError:
                break
            is_single = len(spec.slots) <= 1
            pset = set()
            for sp in sweep_set:
                for gpos, grot in _find_glyph_placements(sp, gname):
                    pset.add((gpos, 0 if is_single else grot))
                if is_single:
                    pset.add((sp, 0))
                else:
                    for grot in range(6):
                        pset.add((sp, grot))
            glyph_options.append(list(pset))
        if len(glyph_options) != len(glyph_names):
            continue

        # Pre-compute per-arm_rot bonder placements (slot overlaps tip)
        bonder_by_armrot = {}
        if need_bonder:
            for arm_rot_c in range(6):
                candidate_tip = sweep_tips[arm_rot_c]
                bset = set()
                for bname in [bonder_name, 'bonder']:
                    try:
                        get_glyph_spec(bname)
                    except KeyError:
                        continue
                    # Bonder must have a slot at the tip (where atoms deposit)
                    for bpos, brot in _find_glyph_placements(candidate_tip, bname):
                        bset.add((bname, bpos, brot))
                    # Also try bonder at tip with all rotations
                    for brot in range(6):
                        bset.add((bname, candidate_tip, brot))
                bonder_by_armrot[arm_rot_c] = list(bset)
        else:
            for arm_rot_c in range(6):
                bonder_by_armrot[arm_rot_c] = [(None, None, None)]

        # Build glyph combos (deduplicate when glyph names are identical)
        if len(glyph_names) == 1:
            gcombos = [(g,) for g in glyph_options[0]]
        elif len(glyph_names) == 2 and glyph_names[0] == glyph_names[1]:
            # Same glyph twice: use combinations_with_replacement
            gcombos = list(itertools.combinations_with_replacement(
                glyph_options[0], 2))
        elif len(glyph_names) == 2:
            gcombos = list(itertools.product(glyph_options[0], glyph_options[1]))
        else:
            gcombos = list(itertools.product(*[o[:30] for o in glyph_options]))

        import random
        random.Random(42).shuffle(gcombos)
        for gcombo in gcombos:
            if time.time() > config_deadline:
                break
            gparts = [Part(name=glyph_names[gi], position=gp, rotation=gr)
                      for gi, (gp, gr) in enumerate(gcombo)]

            for arm_rot in range(6):
                if time.time() > config_deadline:
                    break
                tip = sweep_tips[arm_rot]
                bonder_list = bonder_by_armrot[arm_rot]

                for bname, bpos, brot in bonder_list:
                    if time.time() > config_deadline:
                        break
                    bparts = [Part(name=bname, position=bpos, rotation=brot)] if bname else []

                    for out_rot in out_rots:
                        if time.time() > config_deadline:
                            break
                        base_sol = Solution(puzzle_name=puzzle.name,
                                            solution_name="SR")
                        for ii in range(len(puzzle.inputs)):
                            base_sol.parts.append(
                                Part(name='input', position=tip, io_index=ii))
                        base_sol.parts.extend(gparts)
                        base_sol.parts.extend(bparts)
                        base_sol.parts.append(
                            Part(name='out-std', position=tip,
                                 rotation=out_rot, io_index=0))
                        li = {'arm_pos': arm_pos, 'arm_len': arm_len,
                              'arm_rot': arm_rot, 'arm_type': f'arm{arm_len}'}
                        cache = CachedSolutionBase(base_sol, li)

                        for tape in pass_tapes:
                            sol_bytes = cache.splice(tape)
                            result = puzzle_ctx.verify(sol_bytes, cycle_limit=1000)
                            n_checked += 1
                            if result.valid:
                                metrics = _make_metrics(result)
                                score = float(metrics[target]) if target in metrics else float(metrics['sum4'])
                                if best is None or score < best.score:
                                    arm_part = Part(name=f'arm{arm_len}',
                                                    position=arm_pos,
                                                    size=arm_len,
                                                    rotation=arm_rot)
                                    arm_part.set_tape(tape)
                                    final_sol = Solution(
                                        puzzle_name=puzzle.name,
                                        solution_name="SR")
                                    final_sol.parts = list(base_sol.parts) + [arm_part]
                                    best = SearchResult(final_sol, metrics, score)
                                    if verbose:
                                        m = metrics
                                        print(f'  ** Self-return hit: '
                                              f'{m["cost"]}g/{m["cycles"]}c/'
                                              f'{m["area"]}a/{m["instructions"]}i '
                                              f'= {m["sum4"]}s')

    puzzle_ctx.destroy()
    if verbose:
        print(f'  Self-return checked {n_checked} candidates')
    return best if best is not current_best else None


def _generate_pass_through_tapes_compact() -> List[List[int]]:
    """Compact set of pass-through tapes for self-return layout search.

    Fewer tapes than the full set, focusing on the most common patterns:
    simple sweeps (1-4 steps) and sweep-return combos (up to 3 steps each).
    """
    tapes: List[List[int]] = []

    # Simple sweeps: GRAB, N rotations, RESET
    for n in range(1, 5):
        tapes.append([Inst.GRAB] + [Inst.ROTATE_CW] * n + [Inst.RESET])
        tapes.append([Inst.GRAB] + [Inst.ROTATE_CCW] * n + [Inst.RESET])

    # Sweep-and-return: GRAB, N out, M back, RESET (the P013 WR pattern)
    for n_out in range(1, 4):
        for n_back in range(1, 4):
            if n_out == n_back:
                continue
            tapes.append(
                [Inst.GRAB] + [Inst.ROTATE_CW] * n_out
                + [Inst.ROTATE_CCW] * n_back + [Inst.RESET])
            tapes.append(
                [Inst.GRAB] + [Inst.ROTATE_CCW] * n_out
                + [Inst.ROTATE_CW] * n_back + [Inst.RESET])

    return tapes  # ~20 tapes total


def _generate_pass_through_tapes(arm_start_dir: int) -> List[List[int]]:
    """Generate pass-through tapes: GRAB + rotations + RESET/REPEAT (no DROP).

    These patterns sweep the held atom through glyphs which fire on contact.
    The RESET returns the arm to start, depositing the atom at the tip.
    """
    tapes: List[List[int]] = []

    # Simple sweep patterns: GRAB, rotate N steps, RESET
    for n_rot in range(1, 6):
        # CW sweeps
        tapes.append([Inst.GRAB] + [Inst.ROTATE_CW] * n_rot + [Inst.RESET])
        # CCW sweeps
        tapes.append([Inst.GRAB] + [Inst.ROTATE_CCW] * n_rot + [Inst.RESET])

    # Sweep-and-return patterns: GRAB, rotate out, rotate back, RESET
    # This is the P013 WR pattern: GRAB, CCW, CCW, CW, RESET
    for n_out in range(1, 5):
        for n_back in range(1, 5):
            if n_out == n_back:
                continue  # Would return to same position, no glyph visit
            # CW out, CCW back
            tapes.append(
                [Inst.GRAB]
                + [Inst.ROTATE_CW] * n_out
                + [Inst.ROTATE_CCW] * n_back
                + [Inst.RESET])
            # CCW out, CW back
            tapes.append(
                [Inst.GRAB]
                + [Inst.ROTATE_CCW] * n_out
                + [Inst.ROTATE_CW] * n_back
                + [Inst.RESET])

    # Repeat-terminal variants of the most common patterns
    for n_rot in range(1, 4):
        tapes.append([Inst.GRAB] + [Inst.ROTATE_CW] * n_rot + [Inst.REPEAT])
        tapes.append([Inst.GRAB] + [Inst.ROTATE_CCW] * n_rot + [Inst.REPEAT])

    return tapes


def _build_seed_tapes(layout: Layout, n_inputs: int,
                      pattern_db: PatternDB,
                      glyphs_needed: List[str],
                      analysis: Optional[PuzzleAnalysis] = None,
                      puzzle: Optional[Puzzle] = None,
                      plan: Optional[ProductionPlan] = None,
                      graph: Optional[StationGraph] = None) -> List[List[int]]:
    """Build seed tapes for GA from multiple sources.

    Sources (priority order):
      0. Graph-compiled tapes (from station graph, highest priority)
      0b. Plan-compiled tapes (from production plan)
      1. Compiled tapes from dataflow analysis
      2. Geometric templates based on layout geometry
      3. Similar tapes from archive pattern DB
      4. Common tape templates from archive
    """
    seed_tapes: List[List[int]] = []
    n_stations = len(layout.stations)

    # Source 0: Graph-compiled tapes (station graph, highest priority)
    if graph is not None:
        from .tape_compiler import compile_tapes_from_graph
        graph_tapes = compile_tapes_from_graph(layout, graph)
        seed_tapes.extend(graph_tapes)

    # Source 0b: Plan-compiled tapes (production planner)
    if plan is not None and plan.atom_routes:
        from .tape_compiler import compile_tapes_from_plan
        plan_tapes = compile_tapes_from_plan(layout, plan)
        seed_tapes.extend(plan_tapes)

    # Source 1: Compiled tapes (dataflow-derived)
    if analysis is not None and puzzle is not None:
        from .tape_compiler import compile_tapes
        compiled = compile_tapes(layout, analysis, puzzle)
        seed_tapes.extend(compiled)

    # Source 1b: Bonding chain tapes (complete multi-atom delivery sequences)
    if analysis is not None and puzzle is not None and analysis.needs_bonding:
        from .tape_compiler import compile_bonding_chain_tapes
        chain_tapes = compile_bonding_chain_tapes(layout, analysis, puzzle)
        seed_tapes.extend(chain_tapes)

    # Source 1c: Beam search tapes (geometry-aware instruction-by-instruction)
    if analysis is not None and puzzle is not None:
        from .tape_compiler import beam_search_tape
        beam_tapes = beam_search_tape(layout, analysis, puzzle)
        seed_tapes.extend(beam_tapes)

    # Source 1d: DL-generated tapes (transformer model)
    try:
        from .dl_inference import get_dl_model, generate_tapes_for_layout
        dl_model = get_dl_model()
        if dl_model is not None:
            dl_tapes = generate_tapes_for_layout(dl_model, layout, beam_width=16, max_len=50)
            seed_tapes.extend(dl_tapes[:20])  # top 20 from DL model
    except (ImportError, Exception):
        pass  # DL model not available or not trained

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
# ARCHIVE-GUIDED SEARCH
# =============================================================================

def _find_archive_dir(puzzle_name: str) -> Optional[str]:
    """Find the archive directory for a puzzle by matching its name."""
    import re
    archive_base = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'tools', 'om-archive')
    if not os.path.isdir(archive_base):
        return None

    # Normalize: strip non-alphanumeric, uppercase
    def _norm(s):
        return re.sub(r'[^A-Z0-9]', '', s.upper())

    target = _norm(puzzle_name)

    for journal_dir in sorted(os.listdir(archive_base)):
        journal_path = os.path.join(archive_base, journal_dir)
        if not os.path.isdir(journal_path):
            continue
        for puzzle_dir in os.listdir(journal_path):
            if _norm(puzzle_dir) == target:
                return os.path.join(journal_path, puzzle_dir)
    return None


def _try_archive_guided_search(
    puzzle: Puzzle, puzzle_path: str, analysis: PuzzleAnalysis,
    puzzle_bytes: bytes, simulator: Simulator,
    target: str = 'sum4',
    time_limit: float = 30.0,
    verbose: bool = False,
    current_best: Optional[SearchResult] = None,
) -> Optional[SearchResult]:
    """Try solving using archive solutions as layout templates.

    Parses archive .solution files, extracts their layouts and tapes,
    then runs multi-arm GA to optimize tapes on those layouts.
    """
    t0 = time.time()
    best = current_best

    archive_dir = _find_archive_dir(puzzle.name)
    if archive_dir is None:
        if verbose:
            print(f'  Archive-guided: no archive found for "{puzzle.name}"')
        return None

    # Parse all archive solutions
    sol_files = sorted(Path(archive_dir).glob('*.solution'))
    if not sol_files:
        return None

    if verbose:
        print(f'  Archive-guided: {len(sol_files)} archive solutions found')

    # Sort by sum4 from filename (parse cost+cycles+area+instr from name)
    def _sum4_from_name(f):
        try:
            parts = f.stem.split('-')
            return (int(parts[0].rstrip('g')) + int(parts[1].rstrip('c'))
                    + int(parts[2].rstrip('a')) + int(parts[3].rstrip('i')))
        except (IndexError, ValueError):
            return 999999
    sol_files.sort(key=_sum4_from_name)

    n_outputs = len(puzzle.outputs)
    n_atoms = sum(len(o.molecule.atoms) for o in puzzle.outputs)
    puzzle_ctx = simulator.create_puzzle_context(puzzle_bytes)

    from .tape_compiler import compile_bonding_loop_tapes, compile_tapes_for_multi_arm

    for fi, sol_file in enumerate(sol_files[:10]):  # top 10 by sum4
        if time.time() - t0 > time_limit:
            break

        try:
            sol = parse_solution_file(str(sol_file))
        except Exception:
            continue

        result = extract_layout_from_solution(sol)
        if result is None:
            continue

        layout, archive_tapes = result
        n_arms = len(layout.arms)

        if verbose and fi == 0:
            print(f'  Archive layout: {n_arms} arms, {len(layout.stations)} stations, cost={layout.cost}')

        if n_arms == 0:
            continue

        # Build seed tape sets: archive tapes + bonding templates + compiled tapes
        seed_tape_sets: List[List[List[int]]] = [[] for _ in range(n_arms)]

        # Source 1: Archive tapes (highest priority)
        for ai in range(n_arms):
            if ai < len(archive_tapes) and archive_tapes[ai]:
                seed_tape_sets[ai].append(archive_tapes[ai])

        # Source 2: Bonding loop templates
        if n_arms >= 2 and analysis.needs_bonding:
            bonding_seeds = compile_bonding_loop_tapes(layout, n_atoms)
            if len(bonding_seeds) >= 2:
                # Assign delivery tapes to arm with inputs, reposition to arm with outputs
                for ai in range(n_arms):
                    has_input = any(
                        layout.stations[si][0] == 'input'
                        for si in layout.arms[ai].station_indices
                        if si < len(layout.stations)
                    )
                    if has_input and bonding_seeds[0]:
                        seed_tape_sets[ai].extend(bonding_seeds[0][:50])
                    elif bonding_seeds[1]:
                        seed_tape_sets[ai].extend(bonding_seeds[1][:50])

        # Source 3: Per-arm compiled tapes
        try:
            compiled = compile_tapes_for_multi_arm(layout, analysis, puzzle)
            for ai in range(min(n_arms, len(compiled))):
                seed_tape_sets[ai].extend(compiled[ai][:30])
        except Exception:
            pass

        # Skip if no seeds for any arm
        if any(not seeds for seeds in seed_tape_sets):
            continue

        # Build cached base
        base_sol = layout.to_solution(puzzle, n_outputs)
        cached = CachedMultiArmSolutionBase(base_sol, layout.arms)

        # Screen: try archive tapes with various start_cycle offsets per arm
        tapes = [seed_tape_sets[ai][0] if seed_tape_sets[ai] else []
                 for ai in range(n_arms)]
        if not any(not t for t in tapes) and not any(_is_obviously_invalid(t) for t in tapes):
            # Try offsets on each arm independently
            for offset_arm in range(n_arms):
                for sc_offset in range(0, 12):
                    if time.time() - t0 > time_limit:
                        break
                    start_cycles = [0] * n_arms
                    start_cycles[offset_arm] = sc_offset
                    try:
                        sol_bytes = cached.splice(tapes, start_cycles)
                        vr = puzzle_ctx.verify(sol_bytes, cycle_limit=2000)
                        if vr.valid:
                            metrics = _make_metrics(vr)
                            score = float(metrics[target]) if target in metrics else float(metrics['sum4'])
                            if best is None or score < best.score:
                                final_sol = layout.add_arms_with_tapes(base_sol, tapes, start_cycles)
                                best = SearchResult(final_sol, metrics, score)
                                if verbose:
                                    m = metrics
                                    print(f'  ** Archive-guided (layout {fi} screen arm{offset_arm} sc={sc_offset}): '
                                          f'{m["cost"]}g/{m["cycles"]}c/'
                                          f'{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')
                    except Exception:
                        pass

        # Screen: cross-product of top seeds with start_cycle offsets
        import itertools as _it
        top_per_arm = [seeds[:8] for seeds in seed_tape_sets]
        combos = list(_it.product(*[range(len(t)) for t in top_per_arm]))
        if len(combos) > 200:
            import random
            random.Random(42).shuffle(combos)
            combos = combos[:200]

        for combo in combos:
            if time.time() - t0 > time_limit:
                break
            tapes = [top_per_arm[ai][combo[ai]] for ai in range(n_arms)]
            if any(_is_obviously_invalid(t) for t in tapes):
                continue
            for sc_offset in [0, 4, 8]:
                start_cycles = [0] + [sc_offset] * (n_arms - 1)
                try:
                    sol_bytes = cached.splice(tapes, start_cycles)
                    vr = puzzle_ctx.verify(sol_bytes, cycle_limit=2000)
                    if vr.valid:
                        metrics = _make_metrics(vr)
                        score = float(metrics[target]) if target in metrics else float(metrics['sum4'])
                        if best is None or score < best.score:
                            final_sol = layout.add_arms_with_tapes(base_sol, tapes, start_cycles)
                            best = SearchResult(final_sol, metrics, score)
                            if verbose:
                                m = metrics
                                print(f'  ** Archive-guided (layout {fi} combo): '
                                      f'{m["cost"]}g/{m["cycles"]}c/'
                                      f'{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')
                except Exception:
                    pass

        # GA optimization on this layout
        if time.time() - t0 < time_limit:
            ga = MultiTapeGA(simulator, GAConfig(
                pop_size=40, max_generations=80, stagnation_limit=25,
                cycle_limit=2000))
            ga_result = ga.optimize(
                cached, seed_tape_sets, puzzle_bytes,
                target=target,
                current_best=best.score if best else None,
                n_arms=n_arms,
            )
            if ga_result is not None and ga_result.valid:
                score = ga_result.fitness
                if best is None or score < best.score:
                    final_sol = layout.add_arms_with_tapes(
                        base_sol, ga_result.tapes, ga_result.start_cycles)
                    best = SearchResult(final_sol, ga_result.metrics, score)
                    if verbose:
                        m = ga_result.metrics
                        print(f'  ** Archive-guided (layout {fi} GA): '
                              f'{m["cost"]}g/{m["cycles"]}c/'
                              f'{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')

    puzzle_ctx.destroy()
    return best if best is not current_best else None


# =============================================================================
# MULTI-ARM ESCALATION
# =============================================================================

def _try_multi_arm_layouts(
    puzzle: Puzzle, analysis: PuzzleAnalysis,
    plans: list, graphs: list,
    puzzle_bytes: bytes, simulator: Simulator,
    target: str = 'sum4',
    time_limit: float = 30.0,
    verbose: bool = False,
    current_best: Optional[SearchResult] = None,
) -> Optional[SearchResult]:
    """Try multi-arm solutions for puzzles that need >6 station directions.

    Generates MultiArmLayout instances with 2+ arms, compiles per-arm tapes,
    and optimizes them jointly via MultiTapeGA.
    """
    t0 = time.time()
    best = current_best

    # Generate multi-arm layouts
    config = LayoutConfig(max_layouts=50, timeout_ms=5000)
    multi_layouts = generate_multi_arm_layouts(puzzle, analysis, plans, graphs, config)

    if not multi_layouts:
        if verbose:
            print(f'  Multi-arm: no multi-arm layouts generated')
        return None

    if verbose:
        print(f'  Multi-arm: {len(multi_layouts)} layouts generated')

    n_outputs = len(puzzle.outputs)
    from .solution import CachedMultiArmSolutionBase
    from .tape_compiler import compile_tapes_for_multi_arm

    for li, layout in enumerate(multi_layouts):
        if time.time() - t0 > time_limit:
            break

        # Build base solution (no arms)
        base_sol = layout.to_solution(puzzle, n_outputs)

        # Compile per-arm seed tapes
        seed_tape_sets = compile_tapes_for_multi_arm(layout, analysis, puzzle)

        # Quick screening: try all combinations of first few seeds per arm
        cached = CachedMultiArmSolutionBase(base_sol, layout.arms)
        puzzle_ctx = simulator.create_puzzle_context(puzzle_bytes)

        # Screen: cross-product of first 5 seeds per arm
        n_arms = len(layout.arms)
        seed_limits = [min(5, len(seeds)) for seeds in seed_tape_sets]

        if all(sl > 0 for sl in seed_limits):
            import itertools as it
            seed_indices = [range(sl) for sl in seed_limits]
            for combo in it.product(*seed_indices):
                if time.time() - t0 > time_limit:
                    break
                tapes = [seed_tape_sets[a][combo[a]] for a in range(n_arms)]
                # Skip if any tape is obviously invalid
                if any(_is_obviously_invalid(t) for t in tapes):
                    continue
                for sc_offset in [0, 1, 2, 3]:
                    start_cycles = [0] + [sc_offset] * (n_arms - 1)
                    sol_bytes = cached.splice(tapes, start_cycles)
                    result = puzzle_ctx.verify(sol_bytes, cycle_limit=1000)
                    if result.valid:
                        metrics = _make_metrics(result)
                        score = float(metrics[target]) if target in metrics else float(metrics['sum4'])
                        if best is None or score < best.score:
                            final_sol = layout.add_arms_with_tapes(
                                base_sol, tapes, start_cycles)
                            best = SearchResult(final_sol, metrics, score)
                            if verbose:
                                m = metrics
                                print(f'  ** Multi-arm (layout {li} screen): '
                                      f'{m["cost"]}g/{m["cycles"]}c/'
                                      f'{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')

        # GA optimization
        if time.time() - t0 < time_limit:
            ga = MultiTapeGA(simulator, GAConfig(
                pop_size=20, max_generations=40, stagnation_limit=15))
            ga_result = ga.optimize(
                cached, seed_tape_sets, puzzle_bytes,
                target=target,
                current_best=best.score if best else None,
                n_arms=n_arms,
            )
            if ga_result is not None and ga_result.valid:
                score = ga_result.fitness
                if best is None or score < best.score:
                    final_sol = layout.add_arms_with_tapes(
                        base_sol, ga_result.tapes, ga_result.start_cycles)
                    best = SearchResult(final_sol, ga_result.metrics, score)
                    if verbose:
                        m = ga_result.metrics
                        print(f'  ** Multi-arm (layout {li} GA): '
                              f'{m["cost"]}g/{m["cycles"]}c/'
                              f'{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')

        puzzle_ctx.destroy()

    return best if best is not current_best else None


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
        # Still try if any input molecule matches output atom count
        # (in-place transformation like P022's IRON→COPPER projection)
        has_matching_size = any(
            len(pio.molecule.atoms) == len(puzzle.outputs[0].molecule.atoms)
            for pio in puzzle.inputs
        ) if puzzle.outputs else False
        if not has_matching_size:
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
    # Try regular bonder, bonder-speed, and (if triplex bonds needed) bonder-prisma.
    bonder_types = ['bonder', 'bonder-speed']
    if analysis.needs_bonding:
        # Also try bonder-prisma for triplex bonds
        bonder_types.append('bonder-prisma')

    # Pre-load specs for all bonder types (skip any not in glyph_model)
    bonder_specs: List[Tuple[str, object]] = []
    for bt in bonder_types:
        try:
            bonder_specs.append((bt, get_glyph_spec(bt)))
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

                if analysis.needs_bonding and bonder_specs:
                    # Iterate all bonder types and rotations to include bonder
                    # slots as position candidates
                    bonder_rots = [(bname, bspec, brot)
                                   for bname, bspec in bonder_specs
                                   for brot in range(6)]
                else:
                    bonder_rots = [(None, None, None)]

                for bname, cur_bonder_spec, brot in bonder_rots:
                    # Build candidate positions from glyph slots + bonder slots
                    candidates_raw = list(ia_world) + [glyph_pos]
                    if brot is not None and cur_bonder_spec:
                        for s in cur_bonder_spec.slots:
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
                                        Part(name=bname,
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

    # --- Path 1b: Multi-glyph zero-arm search ---
    # When multiple glyphs are needed, stack them all at ORIGIN and search
    # over rotations for each additional glyph.
    if len(glyphs_needed) >= 2 and (best is None or best.score > theory_min_sum4):
        # Load specs for all needed glyphs
        multi_glyph_specs = []
        for gname in glyphs_needed:
            try:
                multi_glyph_specs.append((gname, get_glyph_spec(gname)))
            except KeyError:
                pass

        if len(multi_glyph_specs) >= 2:
            # First glyph fixed at ORIGIN rotation 0 (translation/rotation symmetry)
            # Additional glyphs try all 6 rotations at ORIGIN (stacked)
            first_name, first_spec = multi_glyph_specs[0]
            rest_specs = multi_glyph_specs[1:]

            # Generate rotation combos for the remaining glyphs (6^(n-1))
            rot_ranges = [range(6) for _ in rest_specs]
            for rot_combo in itertools.product(*rot_ranges):
                if time.time() - t0 > time_limit:
                    break

                # Build glyph parts and collect all slot positions
                glyph_parts = [Part(name=first_name, position=ORIGIN, rotation=0)]
                all_slot_positions = set()

                # Slots from first glyph (rotation 0)
                for s in first_spec.slots:
                    all_slot_positions.add(
                        local_to_world(ORIGIN, 0, s.du, s.dv))

                # Slots from remaining glyphs
                for (gname, gspec), grot in zip(rest_specs, rot_combo):
                    glyph_parts.append(
                        Part(name=gname, position=ORIGIN, rotation=grot))
                    for s in gspec.slots:
                        all_slot_positions.add(
                            local_to_world(ORIGIN, grot, s.du, s.dv))

                # Add ORIGIN itself as a candidate
                all_slot_positions.add(ORIGIN)

                # Determine bonder configs
                if analysis.needs_bonding and bonder_specs:
                    mg_bonder_rots = [(bname, bspec, brot)
                                      for bname, bspec in bonder_specs
                                      for brot in range(6)]
                else:
                    mg_bonder_rots = [(None, None, None)]

                for bname, cur_bonder_spec, brot in mg_bonder_rots:
                    if time.time() - t0 > time_limit:
                        break

                    candidate_positions = list(all_slot_positions)
                    extra_bonder_parts = []

                    if brot is not None and cur_bonder_spec:
                        extra_bonder_parts = [
                            Part(name=bname, position=ORIGIN, rotation=brot)]
                        for s in cur_bonder_spec.slots:
                            bp = local_to_world(ORIGIN, brot, s.du, s.dv)
                            if bp not in all_slot_positions:
                                candidate_positions.append(bp)

                    for input_assignment in itertools.product(
                            candidate_positions, repeat=n_inputs):
                        if time.time() - t0 > time_limit:
                            break
                        input_parts = [
                            Part(name='input', position=input_assignment[i],
                                 io_index=i)
                            for i in range(n_inputs)
                        ]
                        out_candidates = list(
                            set(input_assignment) | all_slot_positions)

                        for out_pos in out_candidates:
                            for out_rot in out_rotations:
                                sol = Solution(
                                    puzzle_name=puzzle.name,
                                    solution_name="ZA")
                                sol.parts = (input_parts + glyph_parts +
                                             extra_bonder_parts + [
                                    Part(name='out-std', position=out_pos,
                                         rotation=out_rot, io_index=0),
                                ])
                                if _check_and_update(sol):
                                    if verbose:
                                        print(f'  Zero-arm (multi-glyph) checked '
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
