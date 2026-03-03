"""Core heuristics for Opus Magnum god-solution generation.

Glyph spatial mechanics (from omsim):
  Directions 0-5 go CW: E(1,0), SE(0,1), SW(-1,1), W(-1,0), NW(0,-1), NE(1,-1)
  CW rotation = direction index - 1; CCW = direction index + 1
  Calcification: active hex at (0,0) — converts cardinal to salt
  Projection: quicksilver at (0,0), metal at (1,0) — promotes metal
  Bonder: bonds atoms at (0,0) and (1,0)
"""
from __future__ import annotations
import os
import subprocess
import tempfile
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple

from .hex import HexCoord, DIRECTIONS, ORIGIN
from .puzzle import AtomType, Puzzle, Molecule, Atom, Bond, BondType, PartFlag
from .solution import Solution, Part, Instruction, Inst, TrackHex, write_solution
from .recipe import PuzzleAnalysis, Reaction, analyze_puzzle, REACTION_GLYPHS


class OptTarget(Enum):
    CYCLES = auto()
    COST = auto()
    AREA = auto()
    INSTRUCTIONS = auto()
    SUM4 = auto()
    BALANCED = auto()


_OMSIM = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tools', 'omsim', 'omsim')
_PUZZLE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tools', 'omsim', 'test', 'puzzle')


def _find_puzzle_path(puzzle_name: str) -> Optional[str]:
    for root, dirs, files in os.walk(_PUZZLE_DIR):
        for f in files:
            if f == f'{puzzle_name}.puzzle':
                return os.path.join(root, f)
    return None


def _verify(sol: Solution, puzzle_path: str) -> Optional[dict]:
    """Verify a solution with omsim. Returns metrics dict or None."""
    sol_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix='.solution', delete=False) as f:
            sol_path = f.name
        write_solution(sol, sol_path)
        result = subprocess.run(
            [_OMSIM, '-p', puzzle_path,
             '-m', 'cycles', '-m', 'cost', '-m', 'area', '-m', 'instructions',
             sol_path],
            capture_output=True, text=True, timeout=30
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


def _score(metrics: dict, target: OptTarget) -> float:
    if target == OptTarget.COST:
        return metrics['cost']
    elif target == OptTarget.CYCLES:
        return metrics['cycles']
    elif target == OptTarget.AREA:
        return metrics['area']
    elif target == OptTarget.INSTRUCTIONS:
        return metrics['instructions']
    return metrics['sum4']


def generate_solution(puzzle: Puzzle, target: OptTarget = OptTarget.COST,
                      puzzle_path: Optional[str] = None) -> Solution:
    """Generate a solution, trying multiple strategies and returning the best."""
    analysis = analyze_puzzle(puzzle)
    if puzzle_path is None:
        puzzle_path = _find_puzzle_path(puzzle.name)

    candidates = []

    # Try each strategy
    for strategy in _get_strategies(puzzle, analysis, target):
        try:
            sol = strategy(puzzle, analysis, target)
            if sol is None:
                continue
            if puzzle_path and os.path.exists(_OMSIM):
                metrics = _verify(sol, puzzle_path)
                if metrics:
                    candidates.append((sol, metrics))
            else:
                candidates.append((sol, None))
        except Exception:
            continue

    if not candidates:
        return _fallback(puzzle, analysis, target)

    if any(m for _, m in candidates):
        # Pick best by target metric
        scored = [(sol, m, _score(m, target)) for sol, m in candidates if m]
        if scored:
            scored.sort(key=lambda x: x[2])
            return scored[0][0]

    return candidates[0][0]


def _get_strategies(puzzle: Puzzle, analysis: PuzzleAnalysis, target: OptTarget) -> list:
    strategies = []
    if _can_zero_arm(puzzle, analysis):
        strategies.append(_solve_zero_arm)
    strategies.append(_solve_single_arm)
    return strategies


# =============================================================================
# ZERO-ARM OVERLAP
# =============================================================================

def _can_zero_arm(puzzle: Puzzle, analysis: PuzzleAnalysis) -> bool:
    if len(puzzle.inputs) != 2:
        return False
    if not all(pio.molecule.is_monoatomic for pio in puzzle.inputs):
        return False
    if len(puzzle.outputs) != 1:
        return False
    out = puzzle.outputs[0].molecule
    if out.atom_count != 2 or len(out.bonds) != 1:
        return False
    if analysis.recipe is None:
        return False
    active = {r: c for r, c in analysis.recipe.reactions.items() if c > 0}
    if len(active) != 1:
        return False
    r = list(active.keys())[0]
    return r in (Reaction.CALCIFICATION, Reaction.PROJECTION)


def _solve_zero_arm(puzzle: Puzzle, analysis: PuzzleAnalysis,
                    target: OptTarget) -> Optional[Solution]:
    """Place inputs/glyph/bonder/output at overlapping positions, no arm needed."""
    sol = Solution(puzzle_name=puzzle.name, solution_name="ZeroArm")
    active = {r: c for r, c in analysis.recipe.reactions.items() if c > 0}
    reaction = list(active.keys())[0]

    pos_a = HexCoord(0, -1)
    pos_b = HexCoord(1, -1)  # = pos_a + DIRECTIONS[0] (E)

    in0_type = puzzle.inputs[0].molecule.atoms[0].atom_type
    in1_type = puzzle.inputs[1].molecule.atoms[0].atom_type

    if reaction == Reaction.CALCIFICATION:
        # Glyph at pos_a converts cardinal→salt. Put the cardinal input at pos_a.
        if in0_type.is_cardinal:
            sol.parts.append(Part(name='input', position=pos_a, io_index=0))
            sol.parts.append(Part(name='input', position=pos_b, io_index=1))
        else:
            sol.parts.append(Part(name='input', position=pos_a, io_index=1))
            sol.parts.append(Part(name='input', position=pos_b, io_index=0))
        sol.parts.append(Part(name='glyph-calcification', position=pos_a, rotation=0))

    elif reaction == Reaction.PROJECTION:
        # Projection: QS at (0,0)=pos_a, metal at (1,0)=pos_b
        if in0_type == AtomType.QUICKSILVER:
            sol.parts.append(Part(name='input', position=pos_a, io_index=0))
            sol.parts.append(Part(name='input', position=pos_b, io_index=1))
        else:
            sol.parts.append(Part(name='input', position=pos_a, io_index=1))
            sol.parts.append(Part(name='input', position=pos_b, io_index=0))
        sol.parts.append(Part(name='glyph-projection', position=pos_a, rotation=0))

    if analysis.needs_bonding:
        sol.parts.append(Part(name='bonder', position=pos_a, rotation=0))

    sol.parts.append(Part(name='out-std', position=pos_a, io_index=0))
    return sol


# =============================================================================
# SINGLE-ARM SOLVER
#
# The workhorse: handles 1-N inputs with various conversion needs.
# Based on the dominant pattern in god-cost solutions.
#
# Key insight: arm at center, each input at a SEPARATE direction from the arm.
# Glyphs placed at other directions. Tape does grab-rotate-drop-reset for each
# atom that needs to be placed.
# =============================================================================

def _solve_single_arm(puzzle: Puzzle, analysis: PuzzleAnalysis,
                      target: OptTarget) -> Optional[Solution]:
    """Single arm1 solver for any puzzle with monoatomic inputs."""
    if not all(pio.molecule.is_monoatomic for pio in puzzle.inputs):
        return None  # TODO: multi-atom input handling

    out_mol = puzzle.outputs[0].molecule if puzzle.outputs else None
    if out_mol is None:
        return None

    n_inputs = len(puzzle.inputs)
    n_outputs = len(puzzle.outputs)

    # Determine glyphs needed
    glyphs_needed = []
    if analysis.recipe:
        for reaction, count in analysis.recipe.reactions.items():
            if count > 0:
                for glyph_name in REACTION_GLYPHS[reaction]:
                    glyphs_needed.append(glyph_name)

    need_bonder = analysis.needs_bonding

    # Total directions needed: inputs + glyphs + 1 (output/bonder area)
    # Max 6 directions around arm
    n_glyph_slots = len(glyphs_needed)
    n_total = n_inputs + n_glyph_slots + 1  # +1 for output/drop zone

    if n_total > 6:
        # Too many stations. Try to overlap glyphs with output.
        n_total = min(6, n_inputs + 1 + (1 if n_glyph_slots > 0 else 0))

    # Build solution
    sol = Solution(puzzle_name=puzzle.name, solution_name="SingleArm")
    arm_pos = ORIGIN

    # Assign direction slots going CW from a starting direction.
    # Convention: inputs get the highest direction indices (furthest CW from output).
    # Output gets direction 0 (E). Glyphs get directions between inputs and output.
    #
    # Example for 1 input + 1 glyph + output:
    #   dir 2: input
    #   dir 1: glyph (calcification)
    #   dir 0: output/bonder
    #   Tape: G (grab at dir 2), R (CW to dir 1, glyph fires), R (CW to dir 0), X (reset)

    output_dir = 0
    # Place glyphs after inputs (in CW order toward output)
    glyph_start_dir = 1
    input_start_dir = glyph_start_dir + n_glyph_slots

    # --- Place inputs ---
    for i in range(n_inputs):
        d = (input_start_dir + i) % 6
        pos = arm_pos + DIRECTIONS[d]
        sol.parts.append(Part(name='input', position=pos, io_index=i))

    # --- Place glyphs ---
    for gi, glyph_name in enumerate(glyphs_needed):
        if gi >= 5:  # safety
            break
        d = (glyph_start_dir + gi) % 6
        pos = arm_pos + DIRECTIONS[d]
        sol.parts.append(Part(name=glyph_name, position=pos, rotation=0))

    # --- Place bonder + output ---
    output_pos = arm_pos + DIRECTIONS[output_dir]
    if need_bonder:
        sol.parts.append(Part(name='bonder', position=output_pos, rotation=output_dir))
    sol.parts.append(Part(name='out-std', position=output_pos, io_index=0))

    # Additional outputs at same position
    for oi in range(1, n_outputs):
        sol.parts.append(Part(name='out-std', position=output_pos, io_index=oi))

    # --- Build arm and tape ---
    # For single-input puzzles: just grab, rotate CW to output, reset
    if n_inputs == 1:
        first_input_dir = input_start_dir % 6
        arm = Part(name='arm1', position=arm_pos, size=1, rotation=first_input_dir)

        # CW steps from input to output
        cw_steps = (first_input_dir - output_dir) % 6

        tape = [Inst.GRAB]
        for _ in range(cw_steps):
            tape.append(Inst.ROTATE_CW)
        tape.append(Inst.RESET)

        arm.set_tape(tape)
        sol.parts.append(arm)
        return sol

    elif n_inputs == 2:
        return _two_input_tape(puzzle, analysis, sol, arm_pos, output_dir,
                               input_start_dir, n_glyph_slots, glyphs_needed, target)

    elif n_inputs >= 3:
        return _multi_input_tape(puzzle, analysis, sol, arm_pos, output_dir,
                                 input_start_dir, n_glyph_slots, target)

    return sol


def _two_input_tape(puzzle: Puzzle, analysis: PuzzleAnalysis,
                    sol: Solution, arm_pos: HexCoord, output_dir: int,
                    input_start_dir: int, n_glyph_slots: int,
                    glyphs_needed: list, target: OptTarget) -> Solution:
    """Build tape for 2-input puzzles.

    Two approaches depending on output molecule:
    A) Both atoms need the same treatment → alternate grab-convert-drop
    B) One atom needs conversion, other doesn't → sequential
    """
    in0_dir = input_start_dir % 6
    in1_dir = (input_start_dir + 1) % 6

    out_mol = puzzle.outputs[0].molecule
    in0_type = puzzle.inputs[0].molecule.atoms[0].atom_type
    in1_type = puzzle.inputs[1].molecule.atoms[0].atom_type

    # Start arm pointing at first input
    arm = Part(name='arm1', position=arm_pos, size=1, rotation=in0_dir)

    # CW steps from each input to output
    cw0_to_out = (in0_dir - output_dir) % 6
    cw1_to_out = (in1_dir - output_dir) % 6
    cw0_to_1 = (in0_dir - in1_dir) % 6  # CW from input0 to input1
    ccw_out_to_0 = (in0_dir - output_dir) % 6  # same as cw0_to_out since we go CCW back

    if out_mol.atom_count == 1:
        # Output is monoatomic — just handle first input
        tape = [Inst.GRAB]
        for _ in range(cw0_to_out):
            tape.append(Inst.ROTATE_CW)
        tape.append(Inst.RESET)
        arm.set_tape(tape)
        sol.parts.append(arm)
        return sol

    if out_mol.atom_count == 2 and analysis.needs_bonding:
        # 2-atom bonded output: grab-convert-drop first atom,
        # then grab-convert-drop second atom on bonder's other hex

        # First atom: grab from input0, rotate CW through glyphs to output area, drop
        tape = [Inst.GRAB]
        for _ in range(cw0_to_out):
            tape.append(Inst.ROTATE_CW)
        tape.append(Inst.DROP)

        # Return to input1: CCW back past glyphs to input1
        # From output_dir, go CCW to in1_dir
        ccw_out_to_1 = (in1_dir - output_dir) % 6
        for _ in range(ccw_out_to_1):
            tape.append(Inst.ROTATE_CCW)
        tape.append(Inst.GRAB)

        # Rotate CW from input1 through (fewer or more) glyphs to output area
        for _ in range(cw1_to_out):
            tape.append(Inst.ROTATE_CW)
        tape.append(Inst.DROP)

        # Reset back to start
        tape.append(Inst.RESET)

        arm.set_tape(tape)
        sol.parts.append(arm)
        return sol

    # For larger outputs, do sequential atom-by-atom placement
    n_atoms = out_mol.atom_count
    tape = []
    for atom_i in range(n_atoms):
        input_idx = atom_i % 2
        input_dir = (input_start_dir + input_idx) % 6

        if atom_i == 0:
            # Already pointing at input0
            pass
        else:
            # Return from output to correct input
            ccw_steps = (input_dir - output_dir) % 6
            for _ in range(ccw_steps):
                tape.append(Inst.ROTATE_CCW)

        tape.append(Inst.GRAB)
        cw_to_out = (input_dir - output_dir) % 6
        for _ in range(cw_to_out):
            tape.append(Inst.ROTATE_CW)
        tape.append(Inst.DROP)

    tape.append(Inst.RESET)
    arm.set_tape(tape)
    sol.parts.append(arm)
    return sol


def _multi_input_tape(puzzle: Puzzle, analysis: PuzzleAnalysis,
                      sol: Solution, arm_pos: HexCoord, output_dir: int,
                      input_start_dir: int, n_glyph_slots: int,
                      target: OptTarget) -> Solution:
    """Build tape for 3+ input puzzles."""
    n_inputs = len(puzzle.inputs)
    out_mol = puzzle.outputs[0].molecule

    arm = Part(name='arm1', position=arm_pos, size=1,
               rotation=input_start_dir % 6)

    tape = []
    n_atoms = out_mol.atom_count

    for atom_i in range(n_atoms):
        input_idx = atom_i % n_inputs
        input_dir = (input_start_dir + input_idx) % 6

        if atom_i > 0:
            # Return from output to input
            ccw_steps = (input_dir - output_dir) % 6
            for _ in range(ccw_steps):
                tape.append(Inst.ROTATE_CCW)

        tape.append(Inst.GRAB)
        cw_to_out = (input_dir - output_dir) % 6
        for _ in range(cw_to_out):
            tape.append(Inst.ROTATE_CW)
        tape.append(Inst.DROP)

    tape.append(Inst.RESET)
    arm.set_tape(tape)
    sol.parts.append(arm)
    return sol


def _fallback(puzzle: Puzzle, analysis: PuzzleAnalysis,
              target: OptTarget) -> Solution:
    """Last-resort fallback: trivial grab-drop."""
    sol = Solution(puzzle_name=puzzle.name, solution_name="Fallback")
    input_pos = DIRECTIONS[1]
    output_pos = DIRECTIONS[0]

    for i in range(len(puzzle.inputs)):
        sol.parts.append(Part(name='input', position=input_pos, io_index=i))
    for i in range(len(puzzle.outputs)):
        sol.parts.append(Part(name='out-std', position=output_pos, io_index=i))

    arm = Part(name='arm1', position=ORIGIN, size=1, rotation=1)
    arm.set_tape([Inst.GRAB, Inst.ROTATE_CW, Inst.DROP, Inst.ROTATE_CCW, Inst.REPEAT])
    sol.parts.append(arm)
    return sol


# =============================================================================
# GOD SOLUTION HEURISTICS
# =============================================================================

@dataclass
class GodHeuristics:
    @staticmethod
    def min_arms_needed(puzzle: Puzzle) -> int:
        return 1

    @staticmethod
    def min_glyphs_needed(analysis: PuzzleAnalysis) -> list:
        glyphs = []
        if analysis.recipe:
            glyphs.extend(analysis.recipe.required_glyphs)
        if analysis.needs_bonding:
            glyphs.append('bonder')
        if analysis.needs_unbonding:
            glyphs.append('unbonder')
        return glyphs

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

    @staticmethod
    def instruction_tape_heuristics(tape: list) -> list:
        if not tape:
            return tape
        for period in range(1, len(tape) // 2 + 1):
            pattern = tape[:period]
            if all(tape[i] == pattern[i % period] for i in range(period, len(tape))):
                return pattern + [Inst.REPEAT]
        return tape
