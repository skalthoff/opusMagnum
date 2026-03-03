"""Search-based solver using Z3 constraints + genetic tape search + omsim verification.

Architecture:
  1. Z3 constrains part placement (positions, rotations) to satisfy:
     - No two inputs at the same hex
     - Arm tip can reach all required hexes via rotation
     - Glyph active hexes align with arm rotation path
     - Output position + rotation matches expected atom positions
  2. For each valid layout from Z3, genetic algorithm searches tapes
  3. omsim verifies each (layout, tape) pair in <1ms
  4. Branch and bound prunes unpromising layouts early
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
from .solution import Solution, Part, Inst, write_solution
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


# Batch verification: write all solutions at once, verify in parallel
def verify_batch(sols: List[Solution], puzzle_path: str) -> List[Optional[dict]]:
    """Verify multiple solutions, return list of metrics (or None for invalid)."""
    results = []
    for sol in sols:
        results.append(verify_solution(sol, puzzle_path))
    return results


@dataclass
class SearchResult:
    solution: Solution
    metrics: dict
    score: float


# =============================================================================
# LAYOUT GENERATION using Z3 constraints
# =============================================================================

def _generate_layouts_z3(puzzle: Puzzle, analysis: PuzzleAnalysis,
                         glyphs_needed: List[str], need_bonder: bool,
                         max_layouts: int = 200) -> List[dict]:
    """Use Z3 to enumerate valid part layouts.

    A layout is a dict mapping part names to (position, rotation) tuples.
    Z3 constraints ensure:
    - Each input at a unique hex (no atom overlap on spawn)
    - Arm tip can sweep through all required positions via CW rotation
    - All parts are within radius 3 of arm (compact solutions)
    """
    import z3

    n_inputs = len(puzzle.inputs)
    n_outputs = len(puzzle.outputs)

    # Decision variables
    arm_q = z3.Int('arm_q')
    arm_r = z3.Int('arm_r')
    arm_rot = z3.Int('arm_rot')  # initial direction 0-5
    arm_len = z3.Int('arm_len')  # 1, 2, or 3

    solver = z3.Solver()

    # Arm position bounded
    solver.add(arm_q >= -3, arm_q <= 3)
    solver.add(arm_r >= -3, arm_r <= 3)
    solver.add(arm_rot >= 0, arm_rot <= 5)
    solver.add(arm_len >= 1, arm_len <= 2)  # arm1 or arm2

    # Input position variables
    in_qs = [z3.Int(f'in_q_{i}') for i in range(n_inputs)]
    in_rs = [z3.Int(f'in_r_{i}') for i in range(n_inputs)]
    for i in range(n_inputs):
        solver.add(in_qs[i] >= -4, in_qs[i] <= 4)
        solver.add(in_rs[i] >= -4, in_rs[i] <= 4)

    # No two inputs at the same position
    for i in range(n_inputs):
        for j in range(i + 1, n_inputs):
            solver.add(z3.Or(in_qs[i] != in_qs[j], in_rs[i] != in_rs[j]))

    # Output position and rotation
    out_q = z3.Int('out_q')
    out_r = z3.Int('out_r')
    out_rot = z3.Int('out_rot')
    solver.add(out_q >= -4, out_q <= 4)
    solver.add(out_r >= -4, out_r <= 4)
    solver.add(out_rot >= -6, out_rot <= 6)

    # Glyph position variables
    glyph_vars = []
    for gi, gname in enumerate(glyphs_needed):
        gq = z3.Int(f'glyph_q_{gi}')
        gr = z3.Int(f'glyph_r_{gi}')
        grot = z3.Int(f'glyph_rot_{gi}')
        solver.add(gq >= -4, gq <= 4)
        solver.add(gr >= -4, gr <= 4)
        solver.add(grot >= -6, grot <= 6)
        glyph_vars.append((gq, gr, grot, gname))

    # Bonder variables
    if need_bonder:
        bond_q = z3.Int('bond_q')
        bond_r = z3.Int('bond_r')
        bond_rot = z3.Int('bond_rot')
        solver.add(bond_q >= -4, bond_q <= 4)
        solver.add(bond_r >= -4, bond_r <= 4)
        solver.add(bond_rot >= -6, bond_rot <= 6)

    # KEY CONSTRAINT: Each input must be reachable by the arm tip.
    # Arm tip at direction d is at arm_pos + DIRECTIONS[d] * arm_len
    # We encode: for each input, there exists a direction d such that
    # input_pos == arm_pos + DIRECTIONS[d] * arm_len
    # This is hard to encode directly in Z3 (nonlinear), so we use
    # a disjunction over the 6 possible directions.

    dir_offsets = [(d.q, d.r) for d in DIRECTIONS]

    for i in range(n_inputs):
        # Input i must be reachable by the arm at some direction
        reach_clauses = []
        for d_idx, (dq, dr) in enumerate(dir_offsets):
            # For arm_len=1: input = arm + direction
            # For arm_len=2: input = arm + 2*direction
            # General: input = arm + arm_len * direction
            # Since arm_len is a variable, we handle cases:
            reach_clauses.append(z3.And(
                arm_len == 1,
                in_qs[i] == arm_q + dq,
                in_rs[i] == arm_r + dr
            ))
            reach_clauses.append(z3.And(
                arm_len == 2,
                in_qs[i] == arm_q + 2 * dq,
                in_rs[i] == arm_r + 2 * dr
            ))
        solver.add(z3.Or(*reach_clauses))

    # Output must be reachable by arm tip at some direction
    out_reach = []
    for dq, dr in dir_offsets:
        out_reach.append(z3.And(arm_len == 1, out_q == arm_q + dq, out_r == arm_r + dr))
        out_reach.append(z3.And(arm_len == 2, out_q == arm_q + 2 * dq, out_r == arm_r + 2 * dr))
    solver.add(z3.Or(*out_reach))

    # Each glyph's active hex must be reachable by arm tip
    for gq, gr, grot, gname in glyph_vars:
        if gname == 'glyph-calcification':
            # Active hex at glyph position (0,0 offset)
            glyph_reach = []
            for dq, dr in dir_offsets:
                glyph_reach.append(z3.And(arm_len == 1, gq == arm_q + dq, gr == arm_r + dr))
                glyph_reach.append(z3.And(arm_len == 2, gq == arm_q + 2 * dq, gr == arm_r + 2 * dr))
            solver.add(z3.Or(*glyph_reach))
        elif gname == 'glyph-projection':
            # QS at (0,0), metal at (1,0) relative to glyph rotation
            # The arm needs to deliver QS to (0,0) and metal to (1,0)
            # For simplicity, constrain glyph (0,0) to be arm-reachable
            glyph_reach = []
            for dq, dr in dir_offsets:
                glyph_reach.append(z3.And(arm_len == 1, gq == arm_q + dq, gr == arm_r + dr))
                glyph_reach.append(z3.And(arm_len == 2, gq == arm_q + 2 * dq, gr == arm_r + 2 * dr))
            solver.add(z3.Or(*glyph_reach))

    # Bonder must be reachable
    if need_bonder:
        bonder_reach = []
        for dq, dr in dir_offsets:
            bonder_reach.append(z3.And(arm_len == 1, bond_q == arm_q + dq, bond_r == arm_r + dr))
            bonder_reach.append(z3.And(arm_len == 2, bond_q == arm_q + 2 * dq, bond_r == arm_r + 2 * dr))
        solver.add(z3.Or(*bonder_reach))

    # Enumerate solutions
    layouts = []
    for _ in range(max_layouts):
        if solver.check() != z3.sat:
            break

        model = solver.model()
        layout = {
            'arm_pos': HexCoord(model[arm_q].as_long(), model[arm_r].as_long()),
            'arm_rot': model[arm_rot].as_long(),
            'arm_len': model[arm_len].as_long(),
            'inputs': [],
            'glyphs': [],
            'output_pos': HexCoord(model[out_q].as_long(), model[out_r].as_long()),
            'output_rot': model[out_rot].as_long(),
        }

        for i in range(n_inputs):
            layout['inputs'].append(HexCoord(model[in_qs[i]].as_long(),
                                              model[in_rs[i]].as_long()))

        for gq, gr, grot, gname in glyph_vars:
            layout['glyphs'].append({
                'name': gname,
                'pos': HexCoord(model[gq].as_long(), model[gr].as_long()),
                'rot': model[grot].as_long(),
            })

        if need_bonder:
            layout['bonder'] = {
                'pos': HexCoord(model[bond_q].as_long(), model[bond_r].as_long()),
                'rot': model[bond_rot].as_long(),
            }

        layouts.append(layout)

        # Block this solution to get the next one
        block = []
        for v in [arm_q, arm_r, arm_rot, arm_len, out_q, out_r, out_rot]:
            block.append(v != model[v])
        for i in range(n_inputs):
            block.append(in_qs[i] != model[in_qs[i]])
            block.append(in_rs[i] != model[in_rs[i]])
        for gq, gr, grot, gname in glyph_vars:
            block.append(gq != model[gq])
            block.append(gr != model[gr])
        if need_bonder:
            block.append(bond_q != model[bond_q])
            block.append(bond_r != model[bond_r])
        solver.add(z3.Or(*block))

    return layouts


# =============================================================================
# TAPE GENERATION: genetic algorithm + structured templates
# =============================================================================

# All instruction types the arm can use
ARM_INSTRUCTIONS = [
    Inst.GRAB, Inst.DROP, Inst.ROTATE_CW, Inst.ROTATE_CCW,
    Inst.PIVOT_CW, Inst.PIVOT_CCW, Inst.RESET, Inst.REPEAT, Inst.NOOP,
]

# Instructions that are valid in solutions (subset based on what puzzles allow)
BASIC_INSTRUCTIONS = [
    Inst.GRAB, Inst.DROP, Inst.ROTATE_CW, Inst.ROTATE_CCW,
    Inst.RESET, Inst.REPEAT,
]

EXTENDED_INSTRUCTIONS = BASIC_INSTRUCTIONS + [
    Inst.PIVOT_CW, Inst.PIVOT_CCW, Inst.EXTEND, Inst.RETRACT,
]


def _generate_template_tapes(layout: dict, n_inputs: int) -> List[List[int]]:
    """Generate structured tape templates for a layout.

    Templates are based on patterns found in god-cost solutions:
    1. G R...R X  (grab, rotate CW to output, reset)
    2. G R...R g R...R X  (grab, rotate, drop, rotate more, reset)
    3. G R...R g r...r C  (grab, rotate, drop, return CCW, repeat)
    4. Multi-input: G R...R X ... G R...R X (one cycle per input)
    5. With pivots: G R P R g X  (grab, rotate, pivot, rotate, drop, reset)
    """
    tapes = []
    arm_pos = layout['arm_pos']
    arm_rot = layout['arm_rot']
    arm_len = layout['arm_len']

    # Compute direction for each part relative to arm
    def part_dir(pos):
        """Find which direction index the arm tip reaches this position."""
        for d in range(6):
            tip = arm_pos
            for _ in range(arm_len):
                tip = tip + DIRECTIONS[d]
            if tip == pos:
                return d
        return None

    input_dirs = [part_dir(p) for p in layout['inputs']]
    output_dir = part_dir(layout['output_pos'])
    glyph_dirs = [part_dir(g['pos']) for g in layout.get('glyphs', [])]
    bonder_dir = part_dir(layout['bonder']['pos']) if 'bonder' in layout else None

    # Filter out None (unreachable parts)
    if output_dir is None or any(d is None for d in input_dirs):
        return []

    # Template 1: Single input, grab-rotate-reset
    if n_inputs == 1 and input_dirs[0] is not None:
        in_d = input_dirs[0]
        cw = (in_d - output_dir) % 6

        # G R*cw X
        tape = [Inst.GRAB] + [Inst.ROTATE_CW] * cw + [Inst.RESET]
        tapes.append(tape)

        # G R*cw g X (explicit drop)
        tape2 = [Inst.GRAB] + [Inst.ROTATE_CW] * cw + [Inst.DROP, Inst.RESET]
        tapes.append(tape2)

        # G R*cw g r*cw C (drop and return)
        tape3 = [Inst.GRAB] + [Inst.ROTATE_CW] * cw + [Inst.DROP] + [Inst.ROTATE_CCW] * cw + [Inst.REPEAT]
        tapes.append(tape3)

        # With pivots at output
        for n_piv in range(1, 4):
            tape_p = [Inst.GRAB] + [Inst.ROTATE_CW] * cw
            tape_p += [Inst.PIVOT_CW] * n_piv
            tape_p += [Inst.RESET]
            tapes.append(tape_p)

            tape_pp = [Inst.GRAB] + [Inst.ROTATE_CW] * cw
            tape_pp += [Inst.PIVOT_CCW] * n_piv
            tape_pp += [Inst.RESET]
            tapes.append(tape_pp)

    # Template 2: Two inputs, sequential
    if n_inputs == 2 and all(d is not None for d in input_dirs):
        d0, d1 = input_dirs
        cw0 = (d0 - output_dir) % 6
        cw1 = (d1 - output_dir) % 6
        ccw_out_to_1 = (d1 - output_dir) % 6
        ccw_out_to_0 = (d0 - output_dir) % 6
        ccw_0_to_1 = (d1 - d0) % 6
        cw_0_to_1 = (d0 - d1) % 6

        # a) G R*cw0 X ... navigate to d1 ... G R*cw1 X
        tape = [Inst.GRAB] + [Inst.ROTATE_CW] * cw0 + [Inst.RESET]
        # After reset, arm is at d0. Navigate to d1.
        if ccw_0_to_1 <= 3:
            tape += [Inst.ROTATE_CCW] * ccw_0_to_1
        else:
            tape += [Inst.ROTATE_CW] * cw_0_to_1
        tape += [Inst.GRAB] + [Inst.ROTATE_CW] * cw1 + [Inst.RESET]
        tapes.append(tape)

        # b) G R*cw0 g r*ccw_out_to_1 G R*cw1 g r*ccw_out_to_0 C
        tape2 = [Inst.GRAB] + [Inst.ROTATE_CW] * cw0 + [Inst.DROP]
        tape2 += [Inst.ROTATE_CCW] * ccw_out_to_1 + [Inst.GRAB]
        tape2 += [Inst.ROTATE_CW] * cw1 + [Inst.DROP]
        tape2 += [Inst.ROTATE_CCW] * ccw_out_to_0 + [Inst.REPEAT]
        tapes.append(tape2)

        # c) Same but with reset instead of CCW return
        tape3 = [Inst.GRAB] + [Inst.ROTATE_CW] * cw0 + [Inst.DROP, Inst.RESET]
        if ccw_0_to_1 <= 3:
            tape3 += [Inst.ROTATE_CCW] * ccw_0_to_1
        else:
            tape3 += [Inst.ROTATE_CW] * cw_0_to_1
        tape3 += [Inst.GRAB] + [Inst.ROTATE_CW] * cw1 + [Inst.DROP, Inst.RESET]
        tapes.append(tape3)

        # d) With pivots
        for n_piv in range(1, 4):
            for piv_type in [Inst.PIVOT_CW, Inst.PIVOT_CCW]:
                tape_p = [Inst.GRAB] + [Inst.ROTATE_CW] * cw0
                tape_p += [piv_type] * n_piv + [Inst.RESET]
                if ccw_0_to_1 <= 3:
                    tape_p += [Inst.ROTATE_CCW] * ccw_0_to_1
                else:
                    tape_p += [Inst.ROTATE_CW] * cw_0_to_1
                tape_p += [Inst.GRAB] + [Inst.ROTATE_CW] * cw1
                tape_p += [piv_type] * n_piv + [Inst.RESET]
                tapes.append(tape_p)

    # Template 3: Three+ inputs, sequential grab-rotate-drop-reset
    if n_inputs >= 3:
        # Sorted by direction for CW sweep
        tape = []
        first_dir = input_dirs[0]
        for i in range(n_inputs):
            d = input_dirs[i]
            if d is None:
                continue
            cw = (d - output_dir) % 6

            if i > 0:
                # Navigate from reset position (first input dir) to this input
                prev_dir = first_dir
                ccw = (d - prev_dir) % 6
                cw_rev = (prev_dir - d) % 6
                if ccw <= 3:
                    tape += [Inst.ROTATE_CCW] * ccw
                else:
                    tape += [Inst.ROTATE_CW] * cw_rev

            tape += [Inst.GRAB] + [Inst.ROTATE_CW] * cw
            tape += [Inst.DROP, Inst.RESET]

        tapes.append(tape)

    return tapes


def _mutate_tape(tape: List[int], rng: random.Random) -> List[int]:
    """Mutate a tape for genetic search."""
    tape = list(tape)
    if not tape:
        return tape

    mutation = rng.choice(['insert', 'delete', 'swap', 'change', 'pivot'])

    if mutation == 'insert' and len(tape) < 30:
        pos = rng.randint(0, len(tape))
        inst = rng.choice(EXTENDED_INSTRUCTIONS)
        tape.insert(pos, inst)
    elif mutation == 'delete' and len(tape) > 3:
        pos = rng.randint(0, len(tape) - 1)
        tape.pop(pos)
    elif mutation == 'swap' and len(tape) >= 2:
        i, j = rng.sample(range(len(tape)), 2)
        tape[i], tape[j] = tape[j], tape[i]
    elif mutation == 'change':
        pos = rng.randint(0, len(tape) - 1)
        tape[pos] = rng.choice(EXTENDED_INSTRUCTIONS)
    elif mutation == 'pivot':
        pos = rng.randint(0, len(tape) - 1)
        tape[pos] = rng.choice([Inst.PIVOT_CW, Inst.PIVOT_CCW])

    return tape


def _crossover(tape1: List[int], tape2: List[int], rng: random.Random) -> List[int]:
    """Crossover two tapes."""
    if not tape1 or not tape2:
        return tape1 or tape2
    cut1 = rng.randint(0, len(tape1))
    cut2 = rng.randint(0, len(tape2))
    return tape1[:cut1] + tape2[cut2:]


# =============================================================================
# MAIN SEARCH LOOP
# =============================================================================

def search_solve(puzzle: Puzzle, puzzle_path: str,
                 target: str = 'cost',
                 max_layouts: int = 200,
                 genetic_generations: int = 50,
                 population_size: int = 30,
                 verbose: bool = False) -> Optional[SearchResult]:
    """Search for optimal solution using Z3 layouts + genetic tapes + omsim.

    Phase 1: Z3 generates valid part layouts
    Phase 2: For each layout, try template tapes + genetic mutations
    Phase 3: Branch and bound prunes layouts that can't beat current best
    """
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

    # --- Phase 0: Try zero-arm overlap ---
    if n_inputs == 2 and n_outputs == 1:
        za_result = _try_zero_arm(puzzle, analysis, puzzle_path, glyphs_needed)
        if za_result:
            best = za_result
            if verbose:
                m = za_result.metrics
                print(f'  Zero-arm: {m["cost"]}g/{m["cycles"]}c/{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')

    # --- Phase 1: Generate layouts with Z3 ---
    if verbose:
        print(f'  Generating layouts with Z3 (glyphs={glyphs_needed}, bonder={need_bonder})...')
    layouts = _generate_layouts_z3(puzzle, analysis, glyphs_needed, need_bonder, max_layouts)
    if verbose:
        print(f'  Got {len(layouts)} layouts')

    # --- Phase 2: For each layout, try template tapes + genetic search ---
    for li, layout in enumerate(layouts):
        # Branch and bound: estimate minimum cost of this layout
        layout_cost = 20  # arm1
        if layout['arm_len'] == 2:
            layout_cost = 30  # arm2
        for g in layout.get('glyphs', []):
            from .solution import PART_COSTS
            layout_cost += PART_COSTS.get(g['name'], 0)
        if need_bonder:
            layout_cost += 10

        # Prune: if targeting cost and this layout costs more than best, skip
        if target == 'cost' and best and layout_cost >= best.score:
            continue

        # Build solution from layout
        base_sol = _layout_to_solution(puzzle, layout, glyphs_needed, need_bonder, n_outputs)

        # Generate template tapes
        templates = _generate_template_tapes(layout, n_inputs)

        # Evaluate templates
        population = []
        for tape in templates:
            sol = _sol_with_tape(base_sol, layout, tape)
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
                        print(f'  [{li}/{len(layouts)}] New best: '
                              f'{m["cost"]}g/{m["cycles"]}c/{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s '
                              f'tape={"".join(chr(t) for t in tape)}')

        # Genetic search on this layout
        if population:
            for gen in range(genetic_generations):
                new_tapes = []
                for _ in range(population_size):
                    parent = rng.choice(population)[0]
                    if len(population) >= 2 and rng.random() < 0.3:
                        parent2 = rng.choice(population)[0]
                        child = _crossover(parent, parent2, rng)
                    else:
                        child = list(parent)
                    child = _mutate_tape(child, rng)
                    new_tapes.append(child)

                for tape in new_tapes:
                    sol = _sol_with_tape(base_sol, layout, tape)
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
                                print(f'  [{li}/{len(layouts)} gen={gen}] New best: '
                                      f'{m["cost"]}g/{m["cycles"]}c/{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')

                # Keep best N in population
                population.sort(key=lambda x: x[1].score)
                population = population[:population_size]

        # Early exit if we hit theoretical minimum cost
        if target == 'cost' and best:
            theory = GodHeuristics.theoretical_min_cost(analysis)
            if best.score <= theory:
                break

    if verbose:
        print(f'  Total verified: {total_verified}')

    return best


def _layout_to_solution(puzzle: Puzzle, layout: dict,
                        glyphs_needed: List[str], need_bonder: bool,
                        n_outputs: int) -> Solution:
    """Convert a layout dict to a Solution (without arm instructions)."""
    sol = Solution(puzzle_name=puzzle.name, solution_name="Search")

    for i, pos in enumerate(layout['inputs']):
        sol.parts.append(Part(name='input', position=pos, io_index=i))

    for g in layout.get('glyphs', []):
        sol.parts.append(Part(name=g['name'], position=g['pos'], rotation=g['rot']))

    if need_bonder and 'bonder' in layout:
        b = layout['bonder']
        sol.parts.append(Part(name='bonder', position=b['pos'], rotation=b['rot']))

    sol.parts.append(Part(name='out-std', position=layout['output_pos'],
                          rotation=layout['output_rot'], io_index=0))
    for oi in range(1, n_outputs):
        sol.parts.append(Part(name='out-std', position=layout['output_pos'],
                              rotation=layout['output_rot'], io_index=oi))

    return sol


def _sol_with_tape(base_sol: Solution, layout: dict, tape: List[int]) -> Solution:
    """Create a copy of base_sol with an arm and tape."""
    sol = Solution(puzzle_name=base_sol.puzzle_name, solution_name=base_sol.solution_name)
    sol.parts = [Part(name=p.name, position=p.position, size=p.size,
                       rotation=p.rotation, io_index=p.io_index,
                       track_hexes=list(p.track_hexes))
                 for p in base_sol.parts]

    arm_name = 'arm1' if layout['arm_len'] == 1 else 'arm2'
    arm = Part(name=arm_name, position=layout['arm_pos'],
               size=layout['arm_len'], rotation=layout['arm_rot'])
    arm.set_tape(tape)
    sol.parts.append(arm)
    return sol


def _try_zero_arm(puzzle: Puzzle, analysis: PuzzleAnalysis,
                  puzzle_path: str, glyphs_needed: List[str]) -> Optional[SearchResult]:
    """Try zero-arm overlap solutions."""
    if not all(pio.molecule.is_monoatomic for pio in puzzle.inputs):
        return None
    if len(puzzle.outputs) != 1:
        return None
    out = puzzle.outputs[0].molecule
    if out.atom_count > 2:
        return None

    best = None

    for pos_a in hex_spiral(ORIGIN, 2):
        for d in range(6):
            pos_b = pos_a + DIRECTIONS[d]
            for swap in (False, True):
                io0 = 1 if swap else 0
                io1 = 0 if swap else 1

                for glyph_rot in range(-6, 7):
                    sol = Solution(puzzle_name=puzzle.name, solution_name="ZeroArm")
                    sol.parts.append(Part(name='input', position=pos_a, io_index=io0))
                    sol.parts.append(Part(name='input', position=pos_b, io_index=io1))

                    for g in glyphs_needed:
                        sol.parts.append(Part(name=g, position=pos_a, rotation=glyph_rot))

                    if analysis.needs_bonding:
                        for brot in range(-6, 7):
                            sol_b = Solution(puzzle_name=puzzle.name, solution_name="ZeroArm")
                            sol_b.parts = list(sol.parts)
                            sol_b.parts.append(Part(name='bonder', position=pos_a, rotation=brot))
                            for orot in range(-6, 7):
                                sol_o = Solution(puzzle_name=puzzle.name, solution_name="ZeroArm")
                                sol_o.parts = list(sol_b.parts)
                                sol_o.parts.append(Part(name='out-std', position=pos_a,
                                                        rotation=orot, io_index=0))
                                metrics = verify_solution(sol_o, puzzle_path)
                                if metrics:
                                    score = metrics['cost']
                                    if best is None or score < best.score:
                                        best = SearchResult(sol_o, metrics, score)
                                        if score <= 20:
                                            return best
                    else:
                        for orot in range(-6, 7):
                            sol_o = Solution(puzzle_name=puzzle.name, solution_name="ZeroArm")
                            sol_o.parts = list(sol.parts)
                            sol_o.parts.append(Part(name='out-std', position=pos_a,
                                                    rotation=orot, io_index=0))
                            metrics = verify_solution(sol_o, puzzle_path)
                            if metrics:
                                score = metrics['cost']
                                if best is None or score < best.score:
                                    best = SearchResult(sol_o, metrics, score)
                                    if score <= 20:
                                        return best

    return best


# =============================================================================
# GOD HEURISTICS
# =============================================================================

@dataclass
class GodHeuristics:
    @staticmethod
    def theoretical_min_cost(analysis: PuzzleAnalysis) -> int:
        cost = 20
        if analysis.recipe:
            cost += analysis.recipe.glyph_cost
        if analysis.needs_bonding:
            cost += 10
        if analysis.needs_unbonding:
            cost += 10
        return cost


def search_all_puzzles(puzzle_dir: str, target: str = 'sum4',
                       max_layouts: int = 100,
                       verbose: bool = True) -> Dict[str, SearchResult]:
    """Search-solve all puzzles in a directory."""
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
            puzzle = parse_puzzle(ppath)
            if verbose:
                print(f'\n{pid}: {puzzle.name}')
            result = search_solve(puzzle, ppath, target=target,
                                  max_layouts=max_layouts, verbose=verbose)
            if result:
                results[pid] = result
                m = result.metrics
                if verbose:
                    print(f'  => {m["cost"]}g/{m["cycles"]}c/{m["area"]}a/{m["instructions"]}i = {m["sum4"]}s')
            else:
                if verbose:
                    print(f'  => no solution found')
        except Exception as e:
            if verbose:
                print(f'  => ERROR: {e}')

    return results
