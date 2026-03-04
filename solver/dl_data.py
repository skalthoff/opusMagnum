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
CONTEXT_DIM = (1                           # n_stations
               + MAX_STATIONS * N_STATION_TYPES  # station types one-hot (40)
               + MAX_STATIONS * 6          # station directions one-hot (48)
               + N_ARM_LEN                 # arm length one-hot (3)
               + N_ARM_TYPE                # arm type one-hot (6)
               + 3                         # n_inputs, n_outputs, n_glyphs
               + N_GLYPH_FLAGS             # glyph type flags (15)
               + 4)                        # needs_bonding, n_total_arms, arm_index, padding
# = 1 + 40 + 48 + 3 + 6 + 3 + 15 + 4 = 120

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
) -> torch.Tensor:
    """Encode layout geometry into a fixed-length feature vector.

    Returns a [CONTEXT_DIM] float tensor.
    """
    vec = torch.zeros(CONTEXT_DIM)
    offset = 0

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


def extract_training_data(archive_dir: str) -> List[TrainingExample]:
    """Extract training examples from all archive solutions.

    Each arm tape in each solution becomes one training example,
    with 6x augmentation via direction rotation.
    """
    from .layout_z3 import extract_layout_from_solution

    archive_path = Path(archive_dir)
    if not archive_path.exists():
        return []

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
                )
                examples.append(TrainingExample(context=context, tokens=tokens))

    return examples


class TapeDataset(Dataset):
    """PyTorch dataset of (context, tape_tokens) pairs."""

    def __init__(self, examples: List[TrainingExample]):
        self.examples = examples

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        ex = self.examples[idx]
        # Pad tokens to MAX_SEQ_LEN
        tokens = ex.tokens[:MAX_SEQ_LEN]
        padded = tokens + [PAD_TOKEN] * (MAX_SEQ_LEN - len(tokens))
        return ex.context, torch.tensor(padded, dtype=torch.long)
