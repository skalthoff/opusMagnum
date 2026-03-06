"""Beam search inference for TapeTransformer.

Generates candidate tapes from a trained model, conditioned on layout geometry.
Integrates with omsim for verification.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Tuple

import torch

if TYPE_CHECKING:
    from .puzzle import Puzzle
    from .recipe import PuzzleAnalysis

from .dl_data import (
    BOS_TOKEN, EOS_TOKEN, PAD_TOKEN, VOCAB_SIZE, MAX_SEQ_LEN,
    CONTEXT_DIM, encode_layout_features, detokenize_tape,
    INST_TO_TOKEN,
)
from .dl_model import TapeTransformer
from .solution import Inst


# Terminal instruction tokens (RESET, REPEAT)
_TERMINAL_TOKENS = {INST_TO_TOKEN[Inst.RESET], INST_TO_TOKEN[Inst.REPEAT]}


def encode_layout(
    layout,
    arm_idx: int = 0,
    analysis: Optional['PuzzleAnalysis'] = None,
    puzzle: Optional['Puzzle'] = None,
) -> torch.Tensor:
    """Convert a Layout or MultiArmLayout into a feature vector for the model.

    Args:
        layout: Layout or MultiArmLayout instance.
        arm_idx: Which arm to encode features for.
        analysis: Optional PuzzleAnalysis for puzzle-aware features.
        puzzle: Optional Puzzle for puzzle-aware features.

    Returns:
        [CONTEXT_DIM] tensor.
    """
    needs_bonding = any(st == 'bonder' for st, _ in layout.stations)
    all_glyphs = [sd for st, sd in layout.stations if st in ('glyph', 'bonder')]

    if hasattr(layout, 'arms') and layout.arms:
        # MultiArmLayout
        arm = layout.arms[arm_idx] if arm_idx < len(layout.arms) else layout.arms[0]
        return encode_layout_features(
            stations=layout.stations,
            directions=layout.directions,
            arm_len=arm.arm_len,
            arm_type=arm.arm_type,
            arm_station_indices=arm.station_indices,
            n_total_arms=len(layout.arms),
            arm_index=arm_idx,
            needs_bonding=needs_bonding,
            all_glyph_names=all_glyphs,
            analysis=analysis,
            puzzle=puzzle,
        )
    else:
        # Single-arm Layout
        return encode_layout_features(
            stations=layout.stations,
            directions=layout.directions,
            arm_len=layout.arm_len,
            arm_type=layout.arm_type,
            arm_station_indices=list(range(len(layout.stations))),
            n_total_arms=1,
            arm_index=0,
            needs_bonding=needs_bonding,
            all_glyph_names=all_glyphs,
            analysis=analysis,
            puzzle=puzzle,
        )


def beam_search_generate(
    model: TapeTransformer,
    context: torch.Tensor,       # [CONTEXT_DIM]
    beam_width: int = 32,
    max_len: int = 60,
    device: str = 'cpu',
) -> List[List[int]]:
    """Generate candidate tapes via beam search.

    Returns a list of instruction tapes (List[int]), sorted by log-probability.
    Beams terminate when they hit a RESET or REPEAT token (or EOS).
    """
    model.eval()
    dev = torch.device(device)
    context = context.to(dev)

    # Initialize beam: [(log_prob, token_sequence)]
    beams: List[Tuple[float, List[int]]] = [(0.0, [BOS_TOKEN])]
    completed: List[Tuple[float, List[int]]] = []

    with torch.no_grad():
        for step in range(max_len):
            if not beams:
                break

            # Batch all active beams
            contexts = context.unsqueeze(0).expand(len(beams), -1)  # [B, CONTEXT_DIM]
            token_seqs = [torch.tensor(b[1], dtype=torch.long) for b in beams]
            max_t = max(len(s) for s in token_seqs)
            padded = torch.zeros(len(beams), max_t, dtype=torch.long, device=dev)
            for i, s in enumerate(token_seqs):
                padded[i, :len(s)] = s.to(dev)

            # Get next-token logits
            logits = model.generate_step(contexts, padded)  # [B, vocab]
            log_probs = torch.log_softmax(logits, dim=-1)

            # Expand beams
            candidates: List[Tuple[float, List[int]]] = []
            for beam_idx, (beam_lp, beam_tokens) in enumerate(beams):
                # Get top-k tokens for this beam
                topk_lp, topk_idx = log_probs[beam_idx].topk(beam_width)
                for k in range(min(beam_width, topk_lp.size(0))):
                    token_id = topk_idx[k].item()
                    new_lp = beam_lp + topk_lp[k].item()
                    new_tokens = beam_tokens + [token_id]

                    # Check if terminal
                    if token_id == EOS_TOKEN or token_id in _TERMINAL_TOKENS:
                        completed.append((new_lp, new_tokens))
                    elif token_id == PAD_TOKEN:
                        continue  # skip pad
                    else:
                        candidates.append((new_lp, new_tokens))

            # Keep top beam_width candidates
            candidates.sort(key=lambda x: -x[0])
            beams = candidates[:beam_width]

            # Early stop if we have enough completed beams
            if len(completed) >= beam_width * 2:
                break

    # Also complete any remaining active beams with RESET
    for lp, tokens in beams:
        completed.append((lp - 1.0, tokens + [INST_TO_TOKEN[Inst.RESET]]))

    # Sort by log-probability (best first)
    completed.sort(key=lambda x: -x[0])

    # Detokenize to instruction tapes
    tapes = []
    seen = set()
    for _, tokens in completed:
        tape = detokenize_tape(tokens)
        if tape and len(tape) >= 2:
            key = tuple(tape)
            if key not in seen:
                seen.add(key)
                tapes.append(tape)

    return tapes


def temperature_sample_generate(
    model: TapeTransformer,
    context: torch.Tensor,       # [CONTEXT_DIM]
    n_samples: int = 64,
    max_len: int = 60,
    temperature: float = 0.8,
    device: str = 'cpu',
) -> List[List[int]]:
    """Generate candidate tapes via temperature sampling.

    Complements beam search by exploring more diverse solutions.
    Returns deduplicated instruction tapes.
    """
    import torch.nn.functional as F

    model.eval()
    dev = torch.device(device)
    context = context.to(dev)

    sequences = torch.full((n_samples, 1), BOS_TOKEN, dtype=torch.long, device=dev)
    ctx_batch = context.unsqueeze(0).expand(n_samples, -1)
    finished = torch.zeros(n_samples, dtype=torch.bool, device=dev)

    with torch.no_grad():
        for step in range(max_len):
            logits = model.generate_step(ctx_batch, sequences)  # [N, vocab]
            logits = logits / max(temperature, 0.01)
            logits[:, PAD_TOKEN] = -1e9

            probs = F.softmax(logits, dim=-1)
            tokens = torch.multinomial(probs, 1)  # [N, 1]
            sequences = torch.cat([sequences, tokens], dim=1)

            for i in range(n_samples):
                if not finished[i]:
                    t = tokens[i].item()
                    if t == EOS_TOKEN or t in _TERMINAL_TOKENS:
                        finished[i] = True
            if finished.all():
                break

    # Detokenize and deduplicate
    tapes = []
    seen = set()
    for i in range(n_samples):
        tape = detokenize_tape(sequences[i].tolist())
        if tape and len(tape) >= 2:
            key = tuple(tape)
            if key not in seen:
                seen.add(key)
                tapes.append(tape)
    return tapes


def generate_tapes_for_layout(
    model: TapeTransformer,
    layout,
    beam_width: int = 32,
    max_len: int = 60,
    device: str = 'cpu',
    analysis: Optional['PuzzleAnalysis'] = None,
    puzzle: Optional['Puzzle'] = None,
    n_temperature_samples: int = 0,
    temperature: float = 0.8,
) -> List[List[int]]:
    """Generate candidate tapes for a layout using the DL model.

    For multi-arm layouts, generates tapes for each arm independently.
    Returns a flat list of all generated tapes (beam search + temperature samples).
    """
    if hasattr(layout, 'arms') and layout.arms:
        all_tapes = []
        for arm_idx in range(len(layout.arms)):
            context = encode_layout(layout, arm_idx,
                                    analysis=analysis, puzzle=puzzle)
            tapes = beam_search_generate(model, context, beam_width, max_len, device)
            if n_temperature_samples > 0:
                tapes.extend(temperature_sample_generate(
                    model, context, n_temperature_samples, max_len,
                    temperature, device))
            all_tapes.extend(tapes)
        return all_tapes
    else:
        context = encode_layout(layout, analysis=analysis, puzzle=puzzle)
        tapes = beam_search_generate(model, context, beam_width, max_len, device)
        if n_temperature_samples > 0:
            tapes.extend(temperature_sample_generate(
                model, context, n_temperature_samples, max_len,
                temperature, device))
        return tapes


def predict_layout_score(
    model: TapeTransformer,
    layout,
    device: str = 'cpu',
    analysis: Optional['PuzzleAnalysis'] = None,
    puzzle: Optional['Puzzle'] = None,
) -> float:
    """Predict sum4 score for a layout using the score head.

    Returns predicted sum4 (lower is better).
    """
    model.eval()
    context = encode_layout(layout, analysis=analysis, puzzle=puzzle)
    with torch.no_grad():
        pred = model.predict_score(context.unsqueeze(0).to(device))
    return pred.item()


def score_and_sort_layouts(
    model: TapeTransformer,
    layouts: list,
    device: str = 'cpu',
    analysis: Optional['PuzzleAnalysis'] = None,
    puzzle: Optional['Puzzle'] = None,
) -> List[Tuple[float, int]]:
    """Score all layouts and return (predicted_sum4, original_index) sorted ascending."""
    model.eval()
    contexts = []
    for layout in layouts:
        if isinstance(layout, tuple):
            layout = layout[0]  # (layout, plan, graph) tuples
        ctx = encode_layout(layout, analysis=analysis, puzzle=puzzle)
        contexts.append(ctx)

    if not contexts:
        return []

    batch = torch.stack(contexts).to(device)
    with torch.no_grad():
        scores = model.predict_score(batch)  # [N]

    scored = [(scores[i].item(), i) for i in range(len(layouts))]
    scored.sort(key=lambda x: x[0])
    return scored


# ---------------------------------------------------------------------------
# Model loading (cached singleton)
# ---------------------------------------------------------------------------

_dl_model: Optional[TapeTransformer] = None
_dl_device: str = 'cpu'


def _auto_detect_device() -> str:
    """Auto-detect best available device: CUDA > MPS > CPU."""
    if torch.cuda.is_available():
        return 'cuda'
    try:
        if torch.backends.mps.is_available():
            return 'mps'
    except AttributeError:
        pass
    return 'cpu'


def get_dl_model(device: Optional[str] = None) -> Optional[TapeTransformer]:
    """Load the trained model (cached). Returns None if no checkpoint exists.

    Tries RL checkpoint first, then supervised checkpoint.
    Auto-detects GPU if device is None.
    """
    global _dl_model, _dl_device

    if device is None:
        device = _auto_detect_device()

    if _dl_model is not None and _dl_device == device:
        return _dl_model

    ckpt_dir = Path(__file__).parent / 'checkpoints'

    # Prefer RL-finetuned checkpoint
    for ckpt_name in ['tape_transformer_rl.pt', 'tape_transformer.pt']:
        checkpoint_path = ckpt_dir / ckpt_name
        if checkpoint_path.exists():
            try:
                _dl_model = TapeTransformer.load(str(checkpoint_path), device=device)
                _dl_model = _dl_model.to(device)
                _dl_device = device
                return _dl_model
            except Exception:
                continue

    return None
