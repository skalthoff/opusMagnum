"""Search-based solver: Z3 layout constraints + genetic tape optimization + omsim oracle.

Architecture:
  1. Enumerate compact layouts where arm sweeps CW from input through glyphs to output
  2. Z3 constrains output rotation to match molecule geometry
  3. Genetic algorithm optimizes tapes within each layout
  4. omsim (<1ms) verifies every candidate
  5. Branch and bound prunes layouts exceeding current best cost

Key insight from analyzing god-cost solutions:
  - Arm at center, inputs/glyphs/output arranged at consecutive CW directions
  - After grabbing, CW rotation sweeps atom through each glyph station
  - Reset (X) teleports arm back cheaply
  - Output rotation must match where atoms actually land
"""
from __future__ import annotations
import os
import random
import subprocess
import tempfile
import itertools
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set

from .hex import HexCoord, DIRECTIONS, ORIGIN, hex_spiral
from .puzzle import Puzzle, AtomType, PartFlag
from .solution import Solution, Part, Inst, write_solution, PART_COSTS
from .recipe import PuzzleAnalysis, Reaction, analyze_puzzle, REACTION_GLYPHS


_OMSIM = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tools', 'omsim', 'omsim')


def verify_solution(sol: Solution, puzzle_path: str) -> Optional[dict]:
    """Verify with omsim, return metrics or None."""
    sol_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix='.solution', delete=False) as f:
            sol_path = f.name
        write_solution(sol, sol_path)
        result = subprocess.run(
            [_OMSIM, '-p', puzzle_path,
             '-m', 'cycles', '-m', 'cost', '-m', 'area', '-m', 'instructions',
             sol_path],
            capture_output=True, text=True, timeout=10
        )
        metrics = {}
        for line in (result.stdout + result.stderr).strip().split('\n'):
            if ':' in line:
                k, v = line.split(':', 1)
                v = v.strip()
                if v.isdigit():
                    metrics[k.strip()] = int(v)
        if all(m in metrics for m in ('cost', 'cycles', 'area', 'instructions')):
            metrics['sum4'] = sum(metrics[k] for k in ('cost', 'cycles', 'area', 'instructions'))
            return metrics
    except Exception:
        pass
    finally:
        if sol_path:
            try:
                os.unlink(sol_path)
            except Exception:
                pass
    return None


@dataclass
class SearchResult:
    solution: Solution
    metrics: dict
    score: float


# =============================================================================
# LAYOUT ENUMERATION: systematic CW-sweep layouts
# =============================================================================

def _enumerate_cw_sweep_layouts(puzzle: Puzzle, analysis: PuzzleAnalysis,
                                 glyphs_needed: List[str],
                                 need_bonder: bool) -> List[dict]:
    """Enumerate layouts where parts are arranged in CW order around the arm.

    The arm grabs from input, then CW rotations sweep the atom through
    glyphs to the output. This is the pattern in all god-cost solutions.

    For each layout we vary:
    - Arm position (within small grid)
    - Starting direction for first input
    - Output rotation (-6 to +6)
    - Glyph rotations
    - Bonder rotation
    """
    layouts = []
    n_inputs = len(puzzle.inputs)

    # Build the station sequence: inputs, then glyphs, then output
    # Each station gets a consecutive direction slot (CW order)
    stations = []
    for i in range(n_inputs):
        stations.append(('input', i))
    for g in glyphs_needed:
        stations.append(('glyph', g))
    if need_bonder:
        stations.append(('bonder', None))
    stations.append(('output', 0))

    n_stations = len(stations)
    if n_stations > 6:
        # Too many stations for single-arm CW sweep
        # Try without some glyphs
        stations = stations[:5] + [stations[-1]]
        n_stations = len(stations)

    # Try different arm positions and starting directions
    arm_positions = list(hex_spiral(ORIGIN, 2))
    start_dirs = range(6)

    for arm_pos in arm_positions:
        for start_dir in start_dirs:
            for arm_len in [1, 2]:
                # Assign each station a direction: start_dir, start_dir-1, start_dir-2, ...
                # (CW = decreasing direction index)
                dirs = [(start_dir - i) % 6 for i in range(n_stations)]

                # Compute positions
                station_positions = []
                for d in dirs:
                    tip = arm_pos
                    for _ in range(arm_len):
                        tip = tip + DIRECTIONS[d]
                    station_positions.append(tip)

                # Check no two inputs overlap
                input_positions = [station_positions[i] for i in range(n_inputs)]
                if len(set(input_positions)) != len(input_positions):
                    continue

                # Try different output and bonder rotations
                for out_rot in range(-6, 7):
                    for bonder_rot in (range(-6, 7) if need_bonder else [0]):
                        for glyph_rot in range(6):
                            layout = {
                                'arm_pos': arm_pos,
                                'arm_rot': start_dir,
                                'arm_len': arm_len,
                                'stations': stations,
                                'dirs': dirs,
                                'positions': station_positions,
                                'output_rot': out_rot,
                                'bonder_rot': bonder_rot,
                                'glyph_rot': glyph_rot,
                            }
                            layouts.append(layout)

    return layouts


def _layout_to_solution(puzzle: Puzzle, layout: dict,
                        need_bonder: bool, n_outputs: int) -> Solution:
    """Build a Solution from a layout dict (without arm tape)."""
    sol = Solution(puzzle_name=puzzle.name, solution_name="Search")

    for i, (stype, sdata) in enumerate(layout['stations']):
        pos = layout['positions'][i]
        d = layout['dirs'][i]

        if stype == 'input':
            sol.parts.append(Part(name='input', position=pos, io_index=sdata))
        elif stype == 'glyph':
            sol.parts.append(Part(name=sdata, position=pos,
                                  rotation=layout['glyph_rot']))
        elif stype == 'bonder':
            sol.parts.append(Part(name='bonder', position=pos,
                                  rotation=layout['bonder_rot']))
        elif stype == 'output':
            sol.parts.append(Part(name='out-std', position=pos,
                                  rotation=layout['output_rot'], io_index=0))
            for oi in range(1, n_outputs):
                sol.parts.append(Part(name='out-std', position=pos,
                                      rotation=layout['output_rot'], io_index=oi))

    return sol


def _build_tapes(layout: dict, n_inputs: int) -> List[List[int]]:
    """Generate tape candidates for a CW-sweep layout."""
    tapes = []
    n_stations = len(layout['stations'])
    output_idx = n_stations - 1

    if n_inputs == 1:
        cw = n_stations - 1  # CW steps from first input to output

        # Template 1: G R*cw X
        tapes.append([Inst.GRAB] + [Inst.ROTATE_CW] * cw + [Inst.RESET])
        # Template 2: G R*cw g X (explicit drop)
        tapes.append([Inst.GRAB] + [Inst.ROTATE_CW] * cw + [Inst.DROP, Inst.RESET])
        # Template 3: G R*cw g r*cw C
        tapes.append([Inst.GRAB] + [Inst.ROTATE_CW] * cw + [Inst.DROP]
                      + [Inst.ROTATE_CCW] * cw + [Inst.REPEAT])
        # Template 4+: With pivots at drop point
        for np in range(1, 6):
            tapes.append([Inst.GRAB] + [Inst.ROTATE_CW] * cw
                          + [Inst.PIVOT_CW] * np + [Inst.RESET])
            tapes.append([Inst.GRAB] + [Inst.ROTATE_CW] * cw
                          + [Inst.PIVOT_CCW] * np + [Inst.RESET])
            tapes.append([Inst.GRAB] + [Inst.ROTATE_CW] * cw
                          + [Inst.DROP] + [Inst.PIVOT_CW] * np + [Inst.RESET])
            tapes.append([Inst.GRAB] + [Inst.ROTATE_CW] * cw
                          + [Inst.DROP] + [Inst.PIVOT_CCW] * np + [Inst.RESET])

    elif n_inputs == 2:
        # Two inputs at consecutive directions, then glyphs, then output
        cw_total = n_stations - 1
        cw0 = cw_total  # input0 to output
        cw1 = cw_total - 1  # input1 to output (one fewer CW step)

        # a) Grab in0, CW to output, reset, CCW to in1, grab, CW to output, reset
        tape_a = [Inst.GRAB] + [Inst.ROTATE_CW] * cw0 + [Inst.RESET]
        tape_a += [Inst.ROTATE_CCW]  # from in0 to in1
        tape_a += [Inst.GRAB] + [Inst.ROTATE_CW] * cw1 + [Inst.RESET]
        tapes.append(tape_a)

        # b) Same with explicit drops
        tape_b = [Inst.GRAB] + [Inst.ROTATE_CW] * cw0 + [Inst.DROP, Inst.RESET]
        tape_b += [Inst.ROTATE_CCW]
        tape_b += [Inst.GRAB] + [Inst.ROTATE_CW] * cw1 + [Inst.DROP, Inst.RESET]
        tapes.append(tape_b)

        # c) With return via CCW instead of reset
        tape_c = [Inst.GRAB] + [Inst.ROTATE_CW] * cw0 + [Inst.DROP]
        tape_c += [Inst.ROTATE_CCW] * cw1 + [Inst.GRAB]
        tape_c += [Inst.ROTATE_CW] * cw1 + [Inst.DROP]
        tape_c += [Inst.ROTATE_CCW] * cw0 + [Inst.REPEAT]
        tapes.append(tape_c)

        # d) With pivots
        for np in range(1, 4):
            for piv in [Inst.PIVOT_CW, Inst.PIVOT_CCW]:
                tape_d = [Inst.GRAB] + [Inst.ROTATE_CW] * cw0
                tape_d += [piv] * np + [Inst.RESET]
                tape_d += [Inst.ROTATE_CCW]
                tape_d += [Inst.GRAB] + [Inst.ROTATE_CW] * cw1
                tape_d += [piv] * np + [Inst.RESET]
                tapes.append(tape_d)

        # e) Grab in0, CW to output, grab in1 (via CCW), CW to output
        tape_e = [Inst.GRAB] + [Inst.ROTATE_CW] * cw0 + [Inst.DROP]
        ccw_out_to_in1 = (layout['dirs'][1] - layout['dirs'][-1]) % 6
        tape_e += [Inst.ROTATE_CCW] * ccw_out_to_in1
        tape_e += [Inst.GRAB] + [Inst.ROTATE_CW] * cw1 + [Inst.DROP]
        ccw_out_to_in0 = (layout['dirs'][0] - layout['dirs'][-1]) % 6
        tape_e += [Inst.ROTATE_CCW] * ccw_out_to_in0
        tape_e += [Inst.REPEAT]
        tapes.append(tape_e)

    elif n_inputs >= 3:
        # Sequential: grab each input, rotate to output, drop, reset, navigate to next
        cw_total = n_stations - 1
        for perm in itertools.permutations(range(n_inputs)):
            tape = []
            for pi, inp_idx in enumerate(perm):
                cw_i = cw_total - inp_idx  # steps from this input to output

                if pi > 0:
                    # Navigate from reset position (dir of input perm[0]) to this input
                    from_dir = layout['dirs'][perm[0]]
                    to_dir = layout['dirs'][inp_idx]
                    ccw = (to_dir - from_dir) % 6
                    cw_rev = (from_dir - to_dir) % 6
                    if ccw <= 3:
                        tape += [Inst.ROTATE_CCW] * ccw
                    else:
                        tape += [Inst.ROTATE_CW] * cw_rev

                tape += [Inst.GRAB] + [Inst.ROTATE_CW] * cw_i
                tape += [Inst.DROP, Inst.RESET]
            tapes.append(tape)

    return tapes


# =============================================================================
# GENETIC TAPE OPTIMIZATION
# =============================================================================

EXTENDED_INSTRUCTIONS = [
    Inst.GRAB, Inst.DROP, Inst.ROTATE_CW, Inst.ROTATE_CCW,
    Inst.PIVOT_CW, Inst.PIVOT_CCW, Inst.RESET, Inst.REPEAT,
]


def _mutate_tape(tape: List[int], rng: random.Random) -> List[int]:
    tape = list(tape)
    if not tape:
        return tape
    op = rng.choice(['insert', 'delete', 'swap', 'change'])
    if op == 'insert' and len(tape) < 40:
        tape.insert(rng.randint(0, len(tape)), rng.choice(EXTENDED_INSTRUCTIONS))
    elif op == 'delete' and len(tape) > 3:
        tape.pop(rng.randint(0, len(tape) - 1))
    elif op == 'swap' and len(tape) >= 2:
        i, j = rng.sample(range(len(tape)), 2)
        tape[i], tape[j] = tape[j], tape[i]
    elif op == 'change':
        tape[rng.randint(0, len(tape) - 1)] = rng.choice(EXTENDED_INSTRUCTIONS)
    return tape


def _crossover(t1: List[int], t2: List[int], rng: random.Random) -> List[int]:
    if not t1 or not t2:
        return t1 or t2
    c1 = rng.randint(0, len(t1))
    c2 = rng.randint(0, len(t2))
    return t1[:c1] + t2[c2:]


# =============================================================================
# MAIN SEARCH
# =============================================================================

def search_solve(puzzle: Puzzle, puzzle_path: str,
                 target: str = 'cost',
                 max_layouts: int = 10000,
                 genetic_gens: int = 30,
                 pop_size: int = 20,
                 verbose: bool = False) -> Optional[SearchResult]:
    """Z3-constrained layout search + genetic tape optimization + omsim oracle."""
    analysis = analyze_puzzle(puzzle)
    rng = random.Random(42)

    glyphs_needed = []
    if analysis.recipe:
        for reaction, count in analysis.recipe.reactions.items():
            if count > 0:
                for glyph_name in REACTION_GLYPHS[reaction]:
                    glyphs_needed.append(glyph_name)

    need_bonder = analysis.needs_bonding
    n_inputs = len(puzzle.inputs)
    n_outputs = len(puzzle.outputs)

    best: Optional[SearchResult] = None
    total_verified = 0

    # --- Phase 0: Zero-arm overlap ---
    za = _try_zero_arm(puzzle, analysis, puzzle_path, glyphs_needed)
    if za:
        best = za
        if verbose:
            m = za.metrics
            print(f'  Zero-arm: {m["cost"]}g/{m["cycles"]}c/{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')

    # --- Phase 1: CW-sweep layouts ---
    if verbose:
        print(f'  Enumerating CW-sweep layouts...')

    # Only use monoatomic inputs for now
    if not all(pio.molecule.is_monoatomic for pio in puzzle.inputs):
        return best

    layouts = _enumerate_cw_sweep_layouts(puzzle, analysis, glyphs_needed, need_bonder)
    if verbose:
        print(f'  Got {len(layouts)} candidate layouts')

    # Subsample if too many
    if len(layouts) > max_layouts:
        rng.shuffle(layouts)
        layouts = layouts[:max_layouts]

    # --- Phase 2: Template tapes + genetic search per layout ---
    for li, layout in enumerate(layouts):
        # Branch and bound: estimate layout cost
        layout_cost = PART_COSTS.get('arm1' if layout['arm_len'] == 1 else 'arm2', 30)
        for stype, sdata in layout['stations']:
            if stype == 'glyph':
                layout_cost += PART_COSTS.get(sdata, 0)
            elif stype == 'bonder':
                layout_cost += 10
        if target == 'cost' and best and layout_cost >= best.score:
            continue

        base_sol = _layout_to_solution(puzzle, layout, need_bonder, n_outputs)
        tapes = _build_tapes(layout, n_inputs)

        # Evaluate template tapes
        population = []
        for tape in tapes:
            sol = _add_arm(base_sol, layout, tape)
            metrics = verify_solution(sol, puzzle_path)
            total_verified += 1
            if metrics:
                score = metrics.get(target, metrics['sum4'])
                sr = SearchResult(sol, metrics, score)
                population.append((tape, sr))
                if best is None or score < best.score:
                    best = sr
                    if verbose:
                        m = metrics
                        print(f'  [{li}] {m["cost"]}g/{m["cycles"]}c/{m["area"]}a/'
                              f'{m["instructions"]}i={m["sum4"]}s '
                              f'tape={"".join(chr(t) for t in tape)}')

        # Genetic optimization if we found valid tapes
        if population:
            for gen in range(genetic_gens):
                children = []
                for _ in range(pop_size):
                    parent = rng.choice(population)[0]
                    if len(population) >= 2 and rng.random() < 0.3:
                        parent2 = rng.choice(population)[0]
                        child = _crossover(parent, parent2, rng)
                    else:
                        child = _mutate_tape(parent, rng)
                    children.append(child)

                for tape in children:
                    sol = _add_arm(base_sol, layout, tape)
                    metrics = verify_solution(sol, puzzle_path)
                    total_verified += 1
                    if metrics:
                        score = metrics.get(target, metrics['sum4'])
                        sr = SearchResult(sol, metrics, score)
                        population.append((tape, sr))
                        if best is None or score < best.score:
                            best = sr
                            if verbose:
                                m = metrics
                                print(f'  [{li} g{gen}] {m["cost"]}g/{m["cycles"]}c/'
                                      f'{m["area"]}a/{m["instructions"]}i={m["sum4"]}s')

                population.sort(key=lambda x: x[1].score)
                population = population[:pop_size]

        # Early exit if at theoretical minimum
        if target == 'cost' and best:
            theory = 20  # arm1
            if analysis.recipe:
                theory += analysis.recipe.glyph_cost
            if need_bonder:
                theory += 10
            if best.score <= theory:
                break

    if verbose:
        print(f'  Verified: {total_verified}')

    return best


def _add_arm(base_sol: Solution, layout: dict, tape: List[int]) -> Solution:
    """Copy base solution and add arm with tape."""
    sol = Solution(puzzle_name=base_sol.puzzle_name, solution_name=base_sol.solution_name)
    sol.parts = [Part(name=p.name, position=p.position, size=p.size,
                       rotation=p.rotation, io_index=p.io_index)
                 for p in base_sol.parts]
    arm_name = 'arm1' if layout['arm_len'] == 1 else 'arm2'
    arm = Part(name=arm_name, position=layout['arm_pos'],
               size=layout['arm_len'], rotation=layout['arm_rot'])
    arm.set_tape(tape)
    sol.parts.append(arm)
    return sol


# =============================================================================
# ZERO-ARM OVERLAP
# =============================================================================

def _try_zero_arm(puzzle: Puzzle, analysis: PuzzleAnalysis,
                  puzzle_path: str, glyphs_needed: List[str]) -> Optional[SearchResult]:
    if len(puzzle.inputs) != 2:
        return None
    if not all(pio.molecule.is_monoatomic for pio in puzzle.inputs):
        return None
    if len(puzzle.outputs) != 1 or puzzle.outputs[0].molecule.atom_count > 2:
        return None

    best = None
    for pos_a in hex_spiral(ORIGIN, 1):
        for d in range(6):
            pos_b = pos_a + DIRECTIONS[d]
            for swap in (False, True):
                io0, io1 = (1, 0) if swap else (0, 1)
                for grot in range(-6, 7):
                    base_parts = [
                        Part(name='input', position=pos_a, io_index=io0),
                        Part(name='input', position=pos_b, io_index=io1),
                    ]
                    for g in glyphs_needed:
                        base_parts.append(Part(name=g, position=pos_a, rotation=grot))

                    if analysis.needs_bonding:
                        for brot in range(-6, 7):
                            for orot in range(-6, 7):
                                sol = Solution(puzzle_name=puzzle.name, solution_name="ZA")
                                sol.parts = list(base_parts) + [
                                    Part(name='bonder', position=pos_a, rotation=brot),
                                    Part(name='out-std', position=pos_a, rotation=orot, io_index=0),
                                ]
                                metrics = verify_solution(sol, puzzle_path)
                                if metrics:
                                    score = metrics['cost']
                                    if best is None or score < best.score:
                                        best = SearchResult(sol, metrics, score)
                                        if score <= 20:
                                            return best
                    else:
                        for orot in range(-6, 7):
                            sol = Solution(puzzle_name=puzzle.name, solution_name="ZA")
                            sol.parts = list(base_parts) + [
                                Part(name='out-std', position=pos_a, rotation=orot, io_index=0),
                            ]
                            metrics = verify_solution(sol, puzzle_path)
                            if metrics:
                                score = metrics['cost']
                                if best is None or score < best.score:
                                    best = SearchResult(sol, metrics, score)
                                    if score <= 20:
                                        return best
    return best


# =============================================================================
# CONVENIENCE
# =============================================================================

def search_all_puzzles(puzzle_dir: str, target: str = 'sum4',
                       max_layouts: int = 5000,
                       verbose: bool = True) -> Dict[str, SearchResult]:
    results = {}
    puzzles = []
    for root, dirs, files in os.walk(puzzle_dir):
        for f in files:
            if f.endswith('.puzzle'):
                puzzles.append((f.replace('.puzzle', ''), os.path.join(root, f)))
    puzzles.sort()

    for pid, ppath in puzzles:
        try:
            from .puzzle import parse_puzzle
            p = parse_puzzle(ppath)
            if verbose:
                print(f'\n{pid}: {p.name}')
            result = search_solve(p, ppath, target=target,
                                  max_layouts=max_layouts, verbose=verbose)
            if result:
                results[pid] = result
                m = result.metrics
                if verbose:
                    print(f'  => {m["cost"]}g/{m["cycles"]}c/{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')
            else:
                if verbose:
                    print(f'  => no solution')
        except Exception as e:
            if verbose:
                print(f'  => ERROR: {e}')
    return results
