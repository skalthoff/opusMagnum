"""Core heuristics for Opus Magnum god-solution generation.

This module implements strategies for generating near-optimal solutions
across different optimization targets (cycles, cost, area, instructions).

Solution generation uses a template-based approach: each puzzle complexity
class has a layout template that places parts and generates instruction tapes.
Solutions are verified with omsim (libverify) after generation.

Glyph spatial mechanics (from omsim):
  Directions 0-5 go CW: E(1,0), SE(0,1), SW(-1,1), W(-1,0), NW(0,-1), NE(1,-1)
  CW rotation = direction index - 1
  CCW rotation = direction index + 1
  Glyph relative position: pos + direction_u(rot)*du + direction_v(rot)*dv
  where direction_v(rot) = direction_u(rot+1)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple

from .hex import HexCoord, DIRECTIONS, ORIGIN
from .puzzle import AtomType, Puzzle, Molecule, Atom, Bond, BondType
from .solution import Solution, Part, Instruction, Inst, TrackHex
from .recipe import PuzzleAnalysis, Reaction, analyze_puzzle


class OptTarget(Enum):
    CYCLES = auto()
    COST = auto()
    AREA = auto()
    INSTRUCTIONS = auto()
    BALANCED = auto()


def generate_solution(puzzle: Puzzle, target: OptTarget = OptTarget.COST) -> Solution:
    """Generate a solution for the given puzzle optimized for the target metric."""
    analysis = analyze_puzzle(puzzle)

    if analysis.complexity == "trivial":
        return _solve_trivial(puzzle, analysis, target)
    elif analysis.complexity in ("simple_conversion", "cardinal", "metal_chain",
                                  "quintessence", "vital"):
        return _solve_monoatomic_conversion(puzzle, analysis, target)
    else:
        return _solve_general(puzzle, analysis, target)


# =============================================================================
# TRIVIAL: just move atoms from input to output (no conversion needed)
# =============================================================================

def _solve_trivial(puzzle: Puzzle, analysis: PuzzleAnalysis,
                   target: OptTarget) -> Solution:
    """Solve trivial puzzles: grab from input, rotate to output, drop."""
    sol = Solution(puzzle_name=puzzle.name, solution_name="God-Trivial")

    # Layout: arm at origin, input at one adjacent hex, output at another.
    # Use 1 CW rotation for minimal cycles.
    # Input at direction 1 (SE), output at direction 0 (E).
    # Arm points SE (rot=1) to grab, CW to dir 0 to drop.
    input_pos = DIRECTIONS[1]   # (0, 1) = SE
    output_pos = DIRECTIONS[0]  # (1, 0) = E
    arm_pos = ORIGIN

    for i, pio in enumerate(puzzle.inputs):
        sol.parts.append(Part(name='input', position=input_pos, io_index=i))
    for i, pio in enumerate(puzzle.outputs):
        out_name = 'out-rep' if getattr(pio, 'repeating', False) else 'out-std'
        sol.parts.append(Part(name=out_name, position=output_pos, io_index=i))

    arm = Part(name='arm1', position=arm_pos, size=1, rotation=1)
    tape = [
        Inst.GRAB,
        Inst.ROTATE_CW,    # dir 1 -> 0: tip moves to output
        Inst.DROP,
        Inst.ROTATE_CCW,   # dir 0 -> 1: tip returns to input
        Inst.REPEAT,
    ]
    arm.set_tape(tape)
    sol.parts.append(arm)
    return sol


# =============================================================================
# MONOATOMIC CONVERSION: single-arm rotation through glyphs
# =============================================================================

def _glyph_active_hex(glyph_name: str, glyph_pos: HexCoord, rotation: int,
                      du: int = 0, dv: int = 0) -> HexCoord:
    """Compute absolute hex position for a glyph's relative offset.

    Uses omsim's mechanism_relative_position formula:
      position + direction_u(rotation) * du + direction_v(rotation) * dv
    where direction_v(rot) = direction_u(rot + 1).
    """
    dir_u = DIRECTIONS[rotation % 6]
    dir_v = DIRECTIONS[(rotation + 1) % 6]
    return HexCoord(
        glyph_pos.q + dir_u.q * du + dir_v.q * dv,
        glyph_pos.r + dir_u.r * du + dir_v.r * dv,
    )


# Glyph spatial footprints: (du, dv) offsets for active hexes
# From omsim sim.c apply_glyphs()
GLYPH_FOOTPRINTS = {
    'glyph-calcification':    {'active': [(0, 0)]},
    'glyph-projection':       {'input_qs': (0, 0), 'input_metal': (1, 0)},
    'glyph-life-and-death':   {'consume': [(0, 0), (1, 0)], 'produce': [(0, 1), (1, -1)]},
    'glyph-dispersion':       {'consume': [(0, 0)], 'produce': [(1, 0), (1, -1), (0, -1), (-1, 0)]},
    'glyph-unification':      {'consume': [(0, 1), (-1, 1), (0, -1), (1, -1)], 'produce': [(0, 0)]},
    'glyph-purification':     {'consume': [(0, 0), (1, 0)], 'produce': [(0, 1)]},
    'glyph-duplication':      {'source': (0, 0), 'target': (1, 0)},
    'bonder':                 {'hex_a': (0, 0), 'hex_b': (1, 0)},
    'unbonder':               {'hex_a': (0, 0), 'hex_b': (1, 0)},
}


def _solve_monoatomic_conversion(puzzle: Puzzle, analysis: PuzzleAnalysis,
                                  target: OptTarget) -> Solution:
    """Solve monoatomic conversion puzzles using single-arm rotation strategy.

    Strategy: place arm at center, arrange input/glyphs/output around it so
    the arm can grab from input, rotate through each glyph position to trigger
    conversion, and drop at output.

    For single-glyph puzzles (e.g., calcification only): 3 positions needed
    around arm (input, glyph, output) = 3 rotations.

    For multi-step: chain glyphs along the rotation path.
    """
    sol = Solution(puzzle_name=puzzle.name, solution_name="God-Conv")

    # Determine the sequence of stations the atom must visit
    stations = _plan_stations(puzzle, analysis)

    if len(stations) <= 6:
        return _single_arm_rotation_solver(puzzle, analysis, sol, stations, target)
    else:
        return _track_based_solver(puzzle, analysis, sol, stations, target)


def _plan_stations(puzzle: Puzzle, analysis: PuzzleAnalysis) -> List[dict]:
    """Plan the sequence of stations (input, glyphs, output) an atom must visit.

    Returns a list of station dicts with 'type', 'part_name', etc.
    """
    stations = []

    # Start at input
    stations.append({'type': 'input', 'part_name': 'input', 'io_index': 0})

    # Visit each required glyph
    if analysis.recipe:
        for reaction, count in analysis.recipe.reactions.items():
            if count <= 0:
                continue
            for glyph_name in _get_glyph_parts(reaction):
                stations.append({'type': 'glyph', 'part_name': glyph_name,
                                 'reaction': reaction})

    # Bonding station
    if analysis.needs_bonding:
        stations.append({'type': 'glyph', 'part_name': 'bonder'})

    # End at output
    stations.append({'type': 'output', 'part_name': 'out-std', 'io_index': 0})

    return stations


def _single_arm_rotation_solver(puzzle: Puzzle, analysis: PuzzleAnalysis,
                                 sol: Solution, stations: List[dict],
                                 target: OptTarget) -> Solution:
    """Place stations around a single arm, connected by rotation.

    Layout: arm at origin. Stations placed at consecutive direction indices
    going CW from the arm (dir N, N-1, N-2, ...). Each CW rotation step
    moves the grabbed atom to the next station.

    For calcification-only puzzles:
      dir 2 (SW): input
      dir 1 (SE): calcification glyph active hex
      dir 0 (E):  output
      → 2 CW rotations from input to output
    """
    n_stations = len(stations)
    if n_stations > 6:
        # Fall back to track-based if too many stations
        return _track_based_solver(puzzle, analysis, sol, stations, target)

    arm_pos = ORIGIN

    # Assign each station a direction index.
    # Start at a high direction index and go CW (decreasing).
    # This means: station[0] at dir (n_stations-1), station[1] at dir (n_stations-2), etc.
    start_dir = n_stations - 1
    station_dirs = list(range(start_dir, start_dir - n_stations, -1))
    # Normalize to 0-5
    station_dirs = [d % 6 for d in station_dirs]

    # Place parts at station positions
    for i, station in enumerate(stations):
        direction = station_dirs[i]
        station_pos = arm_pos + DIRECTIONS[direction]

        if station['type'] == 'input':
            sol.parts.append(Part(name='input', position=station_pos,
                                  io_index=station.get('io_index', 0)))
        elif station['type'] == 'output':
            out_name = station.get('part_name', 'out-std')
            sol.parts.append(Part(name=out_name, position=station_pos,
                                  io_index=station.get('io_index', 0)))
        elif station['type'] == 'glyph':
            glyph_name = station['part_name']
            # For simple glyphs (calcification, etc.), the active hex is at (0,0)
            # relative to the glyph position. So place the glyph AT the station.
            if glyph_name == 'glyph-calcification':
                # Calcification: atom placed directly on glyph hex → converted
                sol.parts.append(Part(name=glyph_name, position=station_pos, rotation=0))
            elif glyph_name == 'glyph-projection':
                # Projection: quicksilver at (0,0), metal at (1,0)
                # For now, place projection at station with appropriate rotation
                # so the atom passes through (0,0) = quicksilver position
                sol.parts.append(Part(name=glyph_name, position=station_pos, rotation=0))
            elif glyph_name == 'bonder':
                # Bonder needs two atoms on adjacent hexes.
                # Place bonder so (0,0) is at this station and (1,0) is at adjacent
                sol.parts.append(Part(name=glyph_name, position=station_pos, rotation=direction))
            else:
                sol.parts.append(Part(name=glyph_name, position=station_pos, rotation=0))

    # Create arm pointing at the input station
    input_dir = station_dirs[0]
    arm = Part(name='arm1', position=arm_pos, size=1, rotation=input_dir)

    # Build tape: grab, rotate CW through stations, drop, rotate CCW back
    tape = [Inst.GRAB]
    n_rotations = n_stations - 1  # number of CW steps from input to output
    for _ in range(n_rotations):
        tape.append(Inst.ROTATE_CW)
    tape.append(Inst.DROP)
    for _ in range(n_rotations):
        tape.append(Inst.ROTATE_CCW)
    tape.append(Inst.REPEAT)

    arm.set_tape(tape)
    sol.parts.append(arm)
    return sol


def _track_based_solver(puzzle: Puzzle, analysis: PuzzleAnalysis,
                         sol: Solution, stations: List[dict],
                         target: OptTarget) -> Solution:
    """Track-based solver: arm on a linear track visits each station.

    Layout: all stations in a line. Arm rides track from input end to output end.
    Glyphs placed adjacent to the track so the arm tip sweeps through them.
    """
    arm_row = 1  # arm rides on r=1
    station_row = 0  # stations are on r=0

    # Place stations along q axis
    for i, station in enumerate(stations):
        q = i * 2
        station_pos = HexCoord(q, station_row)

        if station['type'] == 'input':
            sol.parts.append(Part(name='input', position=station_pos,
                                  io_index=station.get('io_index', 0)))
        elif station['type'] == 'output':
            out_name = station.get('part_name', 'out-std')
            sol.parts.append(Part(name=out_name, position=station_pos,
                                  io_index=station.get('io_index', 0)))
        elif station['type'] == 'glyph':
            sol.parts.append(Part(name=station['part_name'], position=station_pos, rotation=0))

    # Track from input to output
    total_q = (len(stations) - 1) * 2
    arm_start_q = 0
    arm_pos = HexCoord(arm_start_q, arm_row)

    track = Part(name='track', position=arm_pos)
    track_hexes = []
    for tq in range(0, total_q + 1):
        track_hexes.append(TrackHex(tq - arm_pos.q, station_row - arm_pos.r))
    track.track_hexes = track_hexes
    sol.parts.append(track)

    # Arm at start of track, pointing up (toward station row)
    # Direction from (q, 1) to (q, 0) is NW = direction 4
    arm = Part(name='arm1', position=arm_pos, size=1, rotation=4)

    # Tape: grab, track fwd to output, drop, track bwd to input, repeat
    tape = [Inst.GRAB]
    for _ in range(total_q):
        tape.append(Inst.TRACK_FWD)
    tape.append(Inst.DROP)
    for _ in range(total_q):
        tape.append(Inst.TRACK_BWD)
    tape.append(Inst.REPEAT)

    arm.set_tape(tape)
    sol.parts.append(arm)
    return sol


# =============================================================================
# GENERAL SOLVER: for complex multi-atom molecule puzzles
# =============================================================================

def _solve_general(puzzle: Puzzle, analysis: PuzzleAnalysis,
                    target: OptTarget) -> Solution:
    """General solver for complex puzzles.

    Falls back to the monoatomic conversion solver for now.
    Complex molecule puzzles need disassemble-convert-reassemble logic.
    """
    return _solve_monoatomic_conversion(puzzle, analysis, target)


def _get_glyph_parts(reaction: Reaction) -> List[str]:
    from .recipe import REACTION_GLYPHS
    return REACTION_GLYPHS[reaction]


# =============================================================================
# GOD SOLUTION HEURISTICS - Theoretical bounds and optimization strategies
# =============================================================================

@dataclass
class GodHeuristics:
    """Collection of heuristics for finding optimal solutions."""

    @staticmethod
    def min_arms_needed(puzzle: Puzzle) -> int:
        return 1

    @staticmethod
    def min_glyphs_needed(analysis: PuzzleAnalysis) -> List[str]:
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
        cost = 20  # arm1
        if analysis.recipe:
            cost += analysis.recipe.glyph_cost
        if analysis.needs_bonding:
            cost += 10
        if analysis.needs_unbonding:
            cost += 10
        return cost

    @staticmethod
    def overlap_potential(puzzle: Puzzle, analysis: PuzzleAnalysis) -> int:
        """Estimate D value (double-consume opportunities) for N-D+L formula."""
        d = 0
        if len(puzzle.outputs) >= 2:
            d += 1
        if analysis.recipe and Reaction.PROJECTION in analysis.recipe.reactions:
            proj_count = analysis.recipe.reactions[Reaction.PROJECTION]
            if proj_count >= 2:
                d += proj_count // 2
        return d

    @staticmethod
    def instruction_tape_heuristics(tape: List[int]) -> List[int]:
        """Find shortest repeating unit and compress with Repeat."""
        if not tape:
            return tape
        for period in range(1, len(tape) // 2 + 1):
            pattern = tape[:period]
            if all(tape[i] == pattern[i % period] for i in range(period, len(tape))):
                return pattern + [Inst.REPEAT]
        return tape
