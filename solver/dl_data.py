"""Data pipeline for DL-guided tape generation.

Converts archive solutions into (layout_features, tape_tokens) training pairs.
Layout features encode the spatial geometry; tape tokens are the instruction sequence.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
from torch.utils.data import Dataset

from .solution import parse_solution, Solution, Inst
from .puzzle import AtomType, Puzzle
from .recipe import PuzzleAnalysis


# ---------------------------------------------------------------------------
# Token vocabulary
# ---------------------------------------------------------------------------

# Map Inst byte codes to token IDs (0 = PAD, 1 = BOS, 2 = EOS, 3+ = instructions)
INST_TO_TOKEN: Dict[int, int] = {}
TOKEN_TO_INST: Dict[int, int] = {}

_INST_CODES = [
    Inst.GRAB, Inst.DROP, Inst.ROTATE_CW, Inst.ROTATE_CCW,
    Inst.PIVOT_CW, Inst.PIVOT_CCW, Inst.EXTEND, Inst.RETRACT,
    Inst.TRACK_FWD, Inst.TRACK_BWD, Inst.RESET, Inst.REPEAT, Inst.NOOP,
]

PAD_TOKEN = 0
BOS_TOKEN = 1
EOS_TOKEN = 2

for i, code in enumerate(_INST_CODES):
    INST_TO_TOKEN[code] = i + 3  # 3, 4, 5, ...
    TOKEN_TO_INST[i + 3] = code

VOCAB_SIZE = len(_INST_CODES) + 3  # PAD + BOS + EOS + 13 instructions = 16
MAX_SEQ_LEN = 200

# Station type encoding
STATION_TYPE_MAP = {'input': 0, 'glyph': 1, 'bonder': 2, 'unbonder': 3, 'output': 4}
N_STATION_TYPES = 5
MAX_STATIONS = 8

# Layout feature dimensions
N_ARM_LEN = 3      # one-hot: 1, 2, 3
N_ARM_TYPE = 6      # arm1, arm2, arm3, arm6, piston, baron
N_GLYPH_FLAGS = 15  # boolean flags for common glyph types
N_ATOM_TYPES = 16   # AtomType enum: SALT(1)..QUINTESSENCE(16)
N_COMPLEXITY = 7    # complexity class one-hot

# Complexity classes mapped to 7-way one-hot
COMPLEXITY_MAP = {
    'trivial': 0, 'rearrange': 0,
    'bond_only': 1,
    'cardinal': 2,
    'moderate': 3, 'simple_conversion': 3,
    'metal_chain': 4,
    'quintessence': 5,
    'complex_multi': 6, 'vital': 6,
}

LAYOUT_DIM = (1                            # n_stations
              + MAX_STATIONS * N_STATION_TYPES  # station types one-hot (40)
              + MAX_STATIONS * 6           # station directions one-hot (48)
              + N_ARM_LEN                  # arm length one-hot (3)
              + N_ARM_TYPE                 # arm type one-hot (6)
              + 3                          # n_inputs, n_outputs, n_glyphs
              + N_GLYPH_FLAGS              # glyph type flags (15)
              + 4)                         # needs_bonding, n_total_arms, arm_index, padding
# = 1 + 40 + 48 + 3 + 6 + 3 + 15 + 4 = 120

PUZZLE_DIM = (N_ATOM_TYPES                 # input element multi-hot (16)
              + N_ATOM_TYPES               # output element multi-hot (16)
              + 3                          # input_atom_count, output_atom_count, output_bond_count
              + N_COMPLEXITY               # complexity class one-hot (7)
              + 2)                         # needs_unbonding, padding
# = 16 + 16 + 3 + 7 + 2 = 44

CONTEXT_DIM = LAYOUT_DIM + PUZZLE_DIM
# = 120 + 44 = 164

ARM_TYPE_MAP = {'arm1': 0, 'arm2': 1, 'arm3': 2, 'arm6': 3, 'piston': 4, 'baron': 5}

GLYPH_NAMES = [
    'glyph-calcification', 'glyph-life-and-death', 'glyph-projection',
    'glyph-dispersion', 'glyph-purification', 'glyph-duplication',
    'glyph-unification', 'glyph-disposal', 'glyph-marker',
    'bonder', 'bonder-speed', 'bonder-prisma', 'unbonder',
    'track', 'pipe',
]


# ---------------------------------------------------------------------------
# Feature encoding
# ---------------------------------------------------------------------------

def encode_layout_features(
    stations: List[Tuple[str, object]],
    directions: List[int],
    arm_len: int,
    arm_type: str,
    arm_station_indices: List[int],
    n_total_arms: int = 1,
    arm_index: int = 0,
    needs_bonding: bool = False,
    all_glyph_names: Optional[List[str]] = None,
    analysis: Optional[PuzzleAnalysis] = None,
    puzzle: Optional[Puzzle] = None,
) -> torch.Tensor:
    """Encode layout geometry + puzzle features into a fixed-length feature vector.

    Returns a [CONTEXT_DIM] float tensor. When analysis/puzzle are None,
    puzzle dims are zeroed out (backward compatible).
    """
    vec = torch.zeros(CONTEXT_DIM)
    offset = 0

    # --- Layout features (LAYOUT_DIM = 120) ---

    # n_stations for this arm
    n_st = min(len(arm_station_indices), MAX_STATIONS)
    vec[offset] = n_st / MAX_STATIONS  # normalized
    offset += 1

    # Station types one-hot (MAX_STATIONS x N_STATION_TYPES)
    for si_idx in range(MAX_STATIONS):
        if si_idx < len(arm_station_indices):
            real_si = arm_station_indices[si_idx]
            if real_si < len(stations):
                stype = stations[real_si][0]
                type_id = STATION_TYPE_MAP.get(stype, 1)  # default glyph
                vec[offset + type_id] = 1.0
        offset += N_STATION_TYPES

    # Station directions one-hot (MAX_STATIONS x 6)
    for si_idx in range(MAX_STATIONS):
        if si_idx < len(arm_station_indices):
            real_si = arm_station_indices[si_idx]
            if real_si < len(directions):
                d = directions[real_si] % 6
                vec[offset + d] = 1.0
        offset += 6

    # Arm length one-hot
    al = min(arm_len, 3) - 1
    if 0 <= al < N_ARM_LEN:
        vec[offset + al] = 1.0
    offset += N_ARM_LEN

    # Arm type one-hot
    at = ARM_TYPE_MAP.get(arm_type, 0)
    vec[offset + at] = 1.0
    offset += N_ARM_TYPE

    # Counts
    n_inputs = sum(1 for st, _ in stations if st == 'input')
    n_outputs = sum(1 for st, _ in stations if st == 'output')
    n_glyphs = sum(1 for st, _ in stations if st in ('glyph', 'bonder', 'unbonder'))
    vec[offset] = n_inputs / 4.0
    vec[offset + 1] = n_outputs / 4.0
    vec[offset + 2] = n_glyphs / 6.0
    offset += 3

    # Glyph type flags
    if all_glyph_names:
        for gi, gname in enumerate(GLYPH_NAMES):
            if gi < N_GLYPH_FLAGS and gname in all_glyph_names:
                vec[offset + gi] = 1.0
    offset += N_GLYPH_FLAGS

    # Global context
    vec[offset] = 1.0 if needs_bonding else 0.0
    vec[offset + 1] = n_total_arms / 6.0
    vec[offset + 2] = arm_index / 6.0
    # offset + 3 is padding (stays 0)
    offset += 4

    # --- Puzzle features (PUZZLE_DIM = 44) ---
    # When analysis/puzzle are absent, these remain zero (backward compat).

    if puzzle is not None and analysis is not None:
        # Input element types: multi-hot over 16 atom types
        for at_type, count in analysis.input_elements.items():
            idx = int(at_type) - 1  # AtomType starts at 1
            if 0 <= idx < N_ATOM_TYPES and count > 0:
                vec[offset + idx] = 1.0
        offset += N_ATOM_TYPES

        # Output element types: multi-hot over 16 atom types
        for at_type, count in analysis.output_elements.items():
            idx = int(at_type) - 1
            if 0 <= idx < N_ATOM_TYPES and count > 0:
                vec[offset + idx] = 1.0
        offset += N_ATOM_TYPES

        # Counts: input_atom_count, output_atom_count, output_bond_count
        total_in_atoms = sum(len(pio.molecule.atoms) for pio in puzzle.inputs)
        total_out_atoms = sum(len(pio.molecule.atoms) for pio in puzzle.outputs)
        total_out_bonds = sum(len(pio.molecule.bonds) for pio in puzzle.outputs)
        vec[offset] = total_in_atoms / 10.0
        vec[offset + 1] = total_out_atoms / 10.0
        vec[offset + 2] = total_out_bonds / 10.0
        offset += 3

        # Complexity class: 7-way one-hot
        comp_idx = COMPLEXITY_MAP.get(analysis.complexity, 3)  # default moderate
        vec[offset + comp_idx] = 1.0
        offset += N_COMPLEXITY

        # needs_unbonding, padding
        vec[offset] = 1.0 if analysis.needs_unbonding else 0.0
        # offset + 1 is padding (stays 0)
    else:
        offset += PUZZLE_DIM

    return vec


def tokenize_tape(tape: List[int]) -> List[int]:
    """Convert instruction tape to token sequence with BOS/EOS."""
    tokens = [BOS_TOKEN]
    for inst in tape:
        if inst in INST_TO_TOKEN:
            tokens.append(INST_TO_TOKEN[inst])
        elif inst == 0:
            continue  # skip empty slots
    tokens.append(EOS_TOKEN)
    return tokens[:MAX_SEQ_LEN]


def detokenize_tape(tokens: List[int]) -> List[int]:
    """Convert token sequence back to instruction tape."""
    tape = []
    for t in tokens:
        if t in TOKEN_TO_INST:
            tape.append(TOKEN_TO_INST[t])
        elif t == EOS_TOKEN:
            break
    return tape


def augment_directions(directions: List[int], rotation: int) -> List[int]:
    """Rotate all directions by `rotation` steps (mod 6)."""
    return [(d + rotation) % 6 for d in directions]


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------

@dataclass
class TrainingExample:
    context: torch.Tensor   # [CONTEXT_DIM]
    tokens: List[int]       # token sequence
    sum4_score: float = 0.0 # sum4 from archive filename (0 = unknown)


def _parse_sum4_from_filename(filename: str) -> float:
    """Parse sum4 score from archive filename like '30g-15c-10a-5i-...'."""
    try:
        stem = Path(filename).stem
        parts = stem.split('-')
        return float(int(parts[0].rstrip('g')) + int(parts[1].rstrip('c'))
                     + int(parts[2].rstrip('a')) + int(parts[3].rstrip('i')))
    except (IndexError, ValueError):
        return 0.0


def _build_puzzle_lookup(puzzle_dir: str) -> Dict[str, str]:
    """Build puzzle_name → puzzle_file_path lookup from puzzle directory."""
    lookup: Dict[str, str] = {}
    puzzle_path = Path(puzzle_dir)
    if not puzzle_path.exists():
        return lookup
    for pf in puzzle_path.rglob('*.puzzle'):
        lookup[pf.stem] = str(pf)
    return lookup


def extract_training_data(
    archive_dir: str,
    puzzle_dir: Optional[str] = None,
) -> List[TrainingExample]:
    """Extract training examples from all archive solutions.

    Each arm tape in each solution becomes one training example,
    with 6x augmentation via direction rotation.

    If puzzle_dir is provided, puzzle analysis features are included
    in the context vector and sum4 scores are parsed from filenames.
    """
    from .layout_z3 import extract_layout_from_solution

    archive_path = Path(archive_dir)
    if not archive_path.exists():
        return []

    # Build puzzle lookup if puzzle_dir provided
    puzzle_lookup: Dict[str, str] = {}
    if puzzle_dir:
        puzzle_lookup = _build_puzzle_lookup(puzzle_dir)

    # Cache analyzed puzzles to avoid re-parsing
    puzzle_cache: Dict[str, Tuple[Puzzle, PuzzleAnalysis]] = {}

    examples: List[TrainingExample] = []

    for sol_file in sorted(archive_path.rglob('*.solution')):
        try:
            sol = parse_solution(str(sol_file))
        except Exception:
            continue

        result = extract_layout_from_solution(sol)
        if result is None:
            continue

        layout, arm_tapes = result
        n_arms = len(layout.arms)

        # Parse sum4 from filename
        sum4 = _parse_sum4_from_filename(str(sol_file))

        # Try to find and analyze the matching puzzle
        puzzle_obj: Optional[Puzzle] = None
        analysis_obj: Optional[PuzzleAnalysis] = None
        if puzzle_lookup and sol.puzzle_name:
            pname = sol.puzzle_name
            if pname not in puzzle_cache:
                pfile = puzzle_lookup.get(pname)
                if pfile:
                    try:
                        from .puzzle import parse_puzzle
                        from .recipe import analyze_puzzle
                        p = parse_puzzle(pfile)
                        a = analyze_puzzle(p)
                        puzzle_cache[pname] = (p, a)
                    except Exception:
                        puzzle_cache[pname] = (None, None)
                else:
                    puzzle_cache[pname] = (None, None)
            cached = puzzle_cache.get(pname)
            if cached:
                puzzle_obj, analysis_obj = cached

        # Collect all glyph names from stations
        all_glyphs = [sd for st, sd in layout.stations
                      if st in ('glyph', 'bonder')]

        # Check if bonding is needed
        needs_bonding = any(st == 'bonder' for st, _ in layout.stations)

        for arm_idx, arm in enumerate(layout.arms):
            tape = arm_tapes[arm_idx] if arm_idx < len(arm_tapes) else []
            if not tape or len(tape) < 2:
                continue

            tokens = tokenize_tape(tape)
            if len(tokens) < 3:  # BOS + at least 1 instruction + EOS
                continue

            # 6x direction rotation augmentation
            for rot in range(6):
                aug_dirs = augment_directions(layout.directions, rot)
                context = encode_layout_features(
                    stations=layout.stations,
                    directions=aug_dirs,
                    arm_len=arm.arm_len,
                    arm_type=arm.arm_type,
                    arm_station_indices=arm.station_indices,
                    n_total_arms=n_arms,
                    arm_index=arm_idx,
                    needs_bonding=needs_bonding,
                    all_glyph_names=all_glyphs,
                    analysis=analysis_obj,
                    puzzle=puzzle_obj,
                )
                examples.append(TrainingExample(
                    context=context, tokens=tokens, sum4_score=sum4))

    return examples


class TapeDataset(Dataset):
    """PyTorch dataset of (context, tape_tokens, sum4_score) triples."""

    def __init__(self, examples: List[TrainingExample]):
        self.examples = examples

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        ex = self.examples[idx]
        # Pad tokens to MAX_SEQ_LEN
        tokens = ex.tokens[:MAX_SEQ_LEN]
        padded = tokens + [PAD_TOKEN] * (MAX_SEQ_LEN - len(tokens))
        return (ex.context,
                torch.tensor(padded, dtype=torch.long),
                torch.tensor(ex.sum4_score, dtype=torch.float32))
