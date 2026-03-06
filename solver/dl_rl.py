"""REINFORCE finetuning loop for TapeTransformer.

Finetunes a pretrained tape model using RL rewards from omsim verification.
Learns to generate tapes that actually solve puzzles, not just imitate archive.

Usage:
    uv run python -m solver.dl_rl --archive-dir tools/om-archive --puzzle-dir tools/omsim/test/puzzle --device cuda
"""
from __future__ import annotations

import argparse
import math
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

from .dl_data import (
    BOS_TOKEN, EOS_TOKEN, PAD_TOKEN, VOCAB_SIZE, MAX_SEQ_LEN,
    CONTEXT_DIM, INST_TO_TOKEN, TOKEN_TO_INST,
    encode_layout_features, detokenize_tape, _build_puzzle_lookup,
)
from .dl_inference import encode_layout
from .dl_model import TapeTransformer
from .puzzle import Puzzle, parse_puzzle
from .recipe import PuzzleAnalysis, analyze_puzzle
from .simulator import Simulator, PuzzleContext
from .solution import (
    parse_solution as parse_solution_file,
    CachedMultiArmSolutionBase, Inst,
)


# Terminal tokens
_TERMINAL_TOKENS = {INST_TO_TOKEN[Inst.RESET], INST_TO_TOKEN[Inst.REPEAT]}


@dataclass
class RLEpisode:
    """One (puzzle, layout) pair for RL training."""
    puzzle_name: str
    puzzle_path: str
    puzzle_bytes: bytes
    puzzle: Puzzle
    analysis: PuzzleAnalysis
    layout: object  # MultiArmLayout
    cached_base: CachedMultiArmSolutionBase
    archive_tapes: List[List[int]]
    archive_sum4: float
    context_per_arm: List[torch.Tensor]  # [n_arms, CONTEXT_DIM]


def _load_episodes(
    archive_dir: str,
    puzzle_dir: str,
    max_per_puzzle: int = 3,
) -> List[RLEpisode]:
    """Load (puzzle, layout) episodes from archive solutions."""
    from .layout_z3 import extract_layout_from_solution
    from .dl_data import _parse_sum4_from_filename

    puzzle_lookup = _build_puzzle_lookup(puzzle_dir)
    archive_path = Path(archive_dir)
    episodes: List[RLEpisode] = []

    # Group solutions by puzzle
    puzzle_sols: Dict[str, List[Path]] = {}
    for sol_file in sorted(archive_path.rglob('*.solution')):
        try:
            sol = parse_solution_file(str(sol_file))
        except Exception:
            continue
        pname = sol.puzzle_name
        if pname not in puzzle_lookup:
            continue
        puzzle_sols.setdefault(pname, []).append(sol_file)

    # Sort each puzzle's solutions by sum4
    for pname, files in puzzle_sols.items():
        files.sort(key=lambda f: _parse_sum4_from_filename(str(f)))

    # Load episodes
    puzzle_cache: Dict[str, Tuple[Puzzle, PuzzleAnalysis, bytes]] = {}

    for pname, files in puzzle_sols.items():
        for sol_file in files[:max_per_puzzle]:
            try:
                sol = parse_solution_file(str(sol_file))
                result = extract_layout_from_solution(sol)
                if result is None:
                    continue
                layout, arm_tapes = result
                if not layout.arms:
                    continue

                # Load/cache puzzle
                if pname not in puzzle_cache:
                    pfile = puzzle_lookup[pname]
                    puzzle = parse_puzzle(pfile)
                    analysis = analyze_puzzle(puzzle)
                    puzzle_bytes = Path(pfile).read_bytes()
                    puzzle_cache[pname] = (puzzle, analysis, puzzle_bytes)

                puzzle, analysis, puzzle_bytes = puzzle_cache[pname]
                sum4 = _parse_sum4_from_filename(str(sol_file))

                # Build cached base
                base_sol = layout.to_solution(puzzle, len(puzzle.outputs))
                cached = CachedMultiArmSolutionBase(base_sol, layout.arms)

                # Encode context per arm
                contexts = []
                for arm_idx in range(len(layout.arms)):
                    ctx = encode_layout(layout, arm_idx,
                                        analysis=analysis, puzzle=puzzle)
                    contexts.append(ctx)

                episodes.append(RLEpisode(
                    puzzle_name=pname,
                    puzzle_path=puzzle_lookup[pname],
                    puzzle_bytes=puzzle_bytes,
                    puzzle=puzzle,
                    analysis=analysis,
                    layout=layout,
                    cached_base=cached,
                    archive_tapes=arm_tapes,
                    archive_sum4=sum4,
                    context_per_arm=contexts,
                ))
            except Exception:
                continue

    return episodes


def sample_tapes(
    model: TapeTransformer,
    context: torch.Tensor,   # [CONTEXT_DIM]
    k: int = 32,
    max_len: int = 60,
    temperature: float = 1.0,
    device: str = 'cpu',
) -> Tuple[List[List[int]], torch.Tensor]:
    """Sample K tapes from the policy via multinomial sampling.

    Returns:
        tapes: List of K instruction tapes (detokenized)
        log_probs: [K] tensor of total log-probabilities per tape
    """
    dev = torch.device(device)
    context = context.to(dev)

    # Start all K sequences with BOS
    sequences = torch.full((k, 1), BOS_TOKEN, dtype=torch.long, device=dev)
    ctx_batch = context.unsqueeze(0).expand(k, -1)  # [K, CONTEXT_DIM]
    total_log_probs = torch.zeros(k, device=dev)
    all_log_probs: List[torch.Tensor] = []  # per-step log probs for PG
    finished = torch.zeros(k, dtype=torch.bool, device=dev)

    for step in range(max_len):
        logits = model.generate_step(ctx_batch, sequences)  # [K, vocab]
        logits = logits / max(temperature, 0.01)

        # Mask PAD token
        logits[:, PAD_TOKEN] = -1e9

        probs = F.softmax(logits, dim=-1)
        log_p = F.log_softmax(logits, dim=-1)

        # Sample
        tokens = torch.multinomial(probs, 1)  # [K, 1]
        token_log_probs = log_p.gather(1, tokens).squeeze(1)  # [K]

        # Only accumulate for unfinished sequences
        total_log_probs += token_log_probs * (~finished).float()
        all_log_probs.append(token_log_probs)

        sequences = torch.cat([sequences, tokens], dim=1)

        # Check for terminals
        for i in range(k):
            if not finished[i]:
                t = tokens[i].item()
                if t == EOS_TOKEN or t in _TERMINAL_TOKENS:
                    finished[i] = True

        if finished.all():
            break

    # Detokenize
    tapes = []
    for i in range(k):
        tape = detokenize_tape(sequences[i].tolist())
        tapes.append(tape)

    return tapes, total_log_probs


def compute_entropy(model: TapeTransformer, context: torch.Tensor,
                    sequences: torch.Tensor, device: str = 'cpu') -> torch.Tensor:
    """Compute mean entropy of the policy for entropy bonus."""
    logits = model(context.unsqueeze(0), sequences.unsqueeze(0))  # [1, seq, vocab]
    probs = F.softmax(logits[0], dim=-1)
    log_probs = F.log_softmax(logits[0], dim=-1)
    entropy = -(probs * log_probs).sum(dim=-1).mean()
    return entropy


def rl_finetune(
    checkpoint_path: str = 'solver/checkpoints/tape_transformer.pt',
    archive_dir: str = 'tools/om-archive',
    puzzle_dir: str = 'tools/omsim/test/puzzle',
    output_path: str = 'solver/checkpoints/tape_transformer_rl.pt',
    epochs: int = 50,
    k_samples: int = 32,
    lr: float = 1e-4,
    device: str = 'cuda',
    temp_start: float = 1.0,
    temp_end: float = 0.3,
    entropy_coeff: float = 0.01,
    score_weight: float = 0.1,
    invalid_penalty: float = 500.0,
    max_episodes_per_epoch: int = 200,
    cycle_limit: int = 2000,
):
    """REINFORCE finetuning of pretrained TapeTransformer.

    For each episode (puzzle, layout):
      1. Sample K tapes from policy
      2. Verify each with omsim
      3. Reward = archive_sum4 - our_sum4 (positive = beating the record)
      4. REINFORCE gradient: (R - baseline) * grad log pi
      5. Score head loss for valid tapes
    """
    # Device setup
    if device == 'cuda' and not torch.cuda.is_available():
        device = 'mps' if torch.backends.mps.is_available() else 'cpu'
    dev = torch.device(device)
    print(f'Device: {dev}', flush=True)

    # Load pretrained model
    print(f'Loading model from {checkpoint_path}...')
    model = TapeTransformer.load(checkpoint_path, device=str(dev))
    model.train()
    model = model.to(dev)
    print(f'Model loaded (context_dim={model.context_dim})')

    # Load episodes
    print(f'Loading episodes from {archive_dir}...')
    t0 = time.time()
    episodes = _load_episodes(archive_dir, puzzle_dir)
    print(f'Loaded {len(episodes)} episodes in {time.time()-t0:.1f}s')

    if not episodes:
        print('No episodes found!')
        return

    # Group by puzzle for efficient PuzzleContext reuse
    puzzle_episodes: Dict[str, List[RLEpisode]] = {}
    for ep in episodes:
        puzzle_episodes.setdefault(ep.puzzle_name, []).append(ep)
    print(f'Puzzles: {len(puzzle_episodes)}')

    # Optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    simulator = Simulator()

    # Stats
    best_mean_reward = float('-inf')
    total_valid = 0
    total_improved = 0
    total_evals = 0

    print(f'\nRL finetuning for {epochs} epochs, K={k_samples} samples/episode...\n')

    for epoch in range(epochs):
        epoch_t0 = time.time()

        # Temperature annealing
        progress = epoch / max(1, epochs - 1)
        temperature = temp_start + (temp_end - temp_start) * progress

        # Shuffle episodes
        ep_list = list(episodes)
        random.shuffle(ep_list)
        ep_list = ep_list[:max_episodes_per_epoch]

        epoch_rewards = []
        epoch_valid = 0
        epoch_improved = 0
        epoch_policy_loss = 0.0
        epoch_score_loss = 0.0
        n_updates = 0

        # Create puzzle contexts (reuse across episodes of same puzzle)
        puzzle_ctxs: Dict[str, PuzzleContext] = {}

        for ep in ep_list:
            if ep.puzzle_name not in puzzle_ctxs:
                puzzle_ctxs[ep.puzzle_name] = simulator.create_puzzle_context(
                    ep.puzzle_bytes)

            puzzle_ctx = puzzle_ctxs[ep.puzzle_name]
            n_arms = len(ep.layout.arms)

            # Sample tapes for each arm independently
            arm_tapes_all: List[List[List[int]]] = []
            arm_log_probs_all: List[torch.Tensor] = []

            for arm_idx in range(n_arms):
                ctx = ep.context_per_arm[arm_idx].to(dev)
                model.eval()
                with torch.no_grad():
                    tapes, log_probs = sample_tapes(
                        model, ctx, k=k_samples, max_len=60,
                        temperature=temperature, device=str(dev))
                arm_tapes_all.append(tapes)
                arm_log_probs_all.append(log_probs)

            # For multi-arm: combine arm 0 tapes with archive tapes for other arms,
            # and also try archive tape for arm 0 with sampled tapes for arm 1, etc.
            rewards = torch.full((k_samples,), -invalid_penalty, device=dev)
            valid_sum4s = []

            for ki in range(k_samples):
                # Use sampled tape for each arm
                tape_combo = [arm_tapes_all[a][ki] for a in range(n_arms)]

                # Skip if any tape is empty
                if any(not t or len(t) < 2 for t in tape_combo):
                    continue

                # Try with various start_cycle offsets
                best_r = -invalid_penalty
                for sc_offset in [0, 2, 4]:
                    start_cycles = [0] + [sc_offset] * (n_arms - 1)
                    try:
                        sol_bytes = ep.cached_base.splice(tape_combo, start_cycles)
                        vr = puzzle_ctx.verify(sol_bytes, cycle_limit=cycle_limit)
                        total_evals += 1
                        if vr.valid:
                            s4 = vr.cost + vr.cycles + vr.area + vr.instructions
                            # Reward: how much better than archive
                            r = ep.archive_sum4 - s4
                            if r > best_r:
                                best_r = r
                                valid_sum4s.append(s4)
                                epoch_valid += 1
                                if r > 0:
                                    epoch_improved += 1
                    except Exception:
                        pass

                rewards[ki] = best_r

            epoch_rewards.extend(rewards.tolist())

            # REINFORCE update (only if we have variance in rewards)
            if rewards.max() > rewards.min():
                model.train()

                # Per-arm policy gradient
                for arm_idx in range(n_arms):
                    ctx = ep.context_per_arm[arm_idx].to(dev)

                    # Re-compute log probs with gradients
                    tapes_for_arm = arm_tapes_all[arm_idx]
                    log_probs_list = []

                    for ki in range(k_samples):
                        tape = tapes_for_arm[ki]
                        if not tape or len(tape) < 2:
                            log_probs_list.append(torch.tensor(0.0, device=dev))
                            continue

                        from .dl_data import tokenize_tape
                        tokens = tokenize_tape(tape)
                        tokens_t = torch.tensor(tokens[:-1], dtype=torch.long,
                                                device=dev).unsqueeze(0)
                        target_t = torch.tensor(tokens[1:], dtype=torch.long,
                                                device=dev)

                        logits = model(ctx.unsqueeze(0), tokens_t)  # [1, seq, vocab]
                        log_p = F.log_softmax(logits[0], dim=-1)
                        # Gather target token log probs
                        token_log_p = log_p.gather(1, target_t.unsqueeze(1)).squeeze(1)
                        # Mask padding
                        mask = target_t != PAD_TOKEN
                        total_lp = (token_log_p * mask.float()).sum()
                        log_probs_list.append(total_lp)

                    log_probs_t = torch.stack(log_probs_list)

                    # Baseline: mean reward
                    baseline = rewards.mean()
                    advantages = rewards - baseline

                    # Policy gradient loss: -E[(R-b) * log pi]
                    policy_loss = -(advantages.detach() * log_probs_t).mean()

                    # Entropy bonus (approximate: use first sample)
                    if tapes_for_arm[0] and len(tapes_for_arm[0]) >= 2:
                        tokens = tokenize_tape(tapes_for_arm[0])
                        tokens_t = torch.tensor(tokens[:-1], dtype=torch.long,
                                                device=dev).unsqueeze(0)
                        ent_logits = model(ctx.unsqueeze(0), tokens_t)
                        ent_probs = F.softmax(ent_logits[0], dim=-1)
                        ent_log_probs = F.log_softmax(ent_logits[0], dim=-1)
                        entropy = -(ent_probs * ent_log_probs).sum(-1).mean()
                    else:
                        entropy = torch.tensor(0.0, device=dev)

                    total_policy_loss = policy_loss - entropy_coeff * entropy

                    # Score head loss for valid samples
                    score_loss = torch.tensor(0.0, device=dev)
                    if valid_sum4s:
                        pred = model.predict_score(ctx.unsqueeze(0))
                        target_s4 = torch.tensor(
                            [sum(valid_sum4s) / len(valid_sum4s)],
                            device=dev)
                        score_loss = F.mse_loss(pred, target_s4)

                    total_loss = total_policy_loss + score_weight * score_loss

                    optimizer.zero_grad()
                    total_loss.backward()
                    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                    optimizer.step()

                    epoch_policy_loss += policy_loss.item()
                    epoch_score_loss += score_loss.item()
                    n_updates += 1

        # Cleanup puzzle contexts
        for ctx in puzzle_ctxs.values():
            ctx.destroy()

        # Stats
        mean_r = sum(epoch_rewards) / max(1, len(epoch_rewards))
        total_valid += epoch_valid
        total_improved += epoch_improved

        elapsed = time.time() - epoch_t0
        avg_ploss = epoch_policy_loss / max(1, n_updates)
        avg_sloss = epoch_score_loss / max(1, n_updates)

        print(f'Epoch {epoch:3d} | mean_R={mean_r:+.1f} | '
              f'valid={epoch_valid}/{len(ep_list)*k_samples} | '
              f'improved={epoch_improved} | '
              f'policy_loss={avg_ploss:.4f} | score_loss={avg_sloss:.1f} | '
              f'temp={temperature:.2f} | {elapsed:.1f}s')

        # Save if improved
        if mean_r > best_mean_reward:
            best_mean_reward = mean_r
            model.save(output_path)
            print(f'  -> Saved checkpoint (mean_R={mean_r:+.1f})')

    print(f'\nRL finetuning complete.')
    print(f'Total evals: {total_evals}, valid: {total_valid}, '
          f'improved: {total_improved}')
    print(f'Best mean reward: {best_mean_reward:+.1f}')
    print(f'Checkpoint: {output_path}')


def main():
    parser = argparse.ArgumentParser(description='RL finetune TapeTransformer')
    parser.add_argument('--checkpoint', default='solver/checkpoints/tape_transformer.pt',
                        help='Path to pretrained checkpoint')
    parser.add_argument('--archive-dir', default='tools/om-archive')
    parser.add_argument('--puzzle-dir', default='tools/omsim/test/puzzle')
    parser.add_argument('--output', default='solver/checkpoints/tape_transformer_rl.pt',
                        help='Output checkpoint path')
    parser.add_argument('--epochs', type=int, default=50)
    parser.add_argument('--k-samples', type=int, default=32)
    parser.add_argument('--lr', type=float, default=1e-4)
    parser.add_argument('--device', default='cuda',
                        choices=['cpu', 'mps', 'cuda'])
    parser.add_argument('--temp-start', type=float, default=1.0)
    parser.add_argument('--temp-end', type=float, default=0.3)
    parser.add_argument('--entropy-coeff', type=float, default=0.01)
    parser.add_argument('--score-weight', type=float, default=0.1)
    parser.add_argument('--invalid-penalty', type=float, default=500.0)
    parser.add_argument('--max-episodes', type=int, default=200,
                        help='Max episodes per epoch')
    parser.add_argument('--cycle-limit', type=int, default=2000)
    args = parser.parse_args()

    rl_finetune(
        checkpoint_path=args.checkpoint,
        archive_dir=args.archive_dir,
        puzzle_dir=args.puzzle_dir,
        output_path=args.output,
        epochs=args.epochs,
        k_samples=args.k_samples,
        lr=args.lr,
        device=args.device,
        temp_start=args.temp_start,
        temp_end=args.temp_end,
        entropy_coeff=args.entropy_coeff,
        score_weight=args.score_weight,
        invalid_penalty=args.invalid_penalty,
        max_episodes_per_epoch=args.max_episodes,
        cycle_limit=args.cycle_limit,
    )


if __name__ == '__main__':
    main()
