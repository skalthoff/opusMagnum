"""Training script for TapeTransformer.

Usage:
    uv run python -m solver.dl_train --archive-dir tools/om-archive --epochs 200 --device cuda
    uv run python -m solver.dl_train --archive-dir tools/om-archive --puzzle-dir tools/omsim/test/puzzle --epochs 200 --device cuda
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split

from .dl_data import (
    extract_training_data, TapeDataset, PAD_TOKEN, MAX_SEQ_LEN, CONTEXT_DIM,
)
from .dl_model import TapeTransformer


def train(
    archive_dir: str = 'tools/om-archive',
    puzzle_dir: str = None,
    epochs: int = 200,
    batch_size: int = 64,
    lr: float = 3e-4,
    device: str = 'cuda',
    checkpoint_dir: str = 'solver/checkpoints',
    patience: int = 20,
    score_weight: float = 0.1,
):
    """Train the TapeTransformer on archive solutions.

    Multi-task loss: tape cross-entropy + score_weight * MSE(pred_sum4, actual_sum4).
    """
    # Device setup
    if device == 'cuda' and not torch.cuda.is_available():
        print('CUDA not available, trying MPS...', flush=True)
        device = 'mps'
    if device == 'mps' and not torch.backends.mps.is_available():
        print('MPS not available, falling back to CPU', flush=True)
        device = 'cpu'
    dev = torch.device(device)
    print(f'Device: {dev}', flush=True)

    # Extract training data
    print(f'Extracting training data from {archive_dir}...')
    if puzzle_dir:
        print(f'  Puzzle features from {puzzle_dir}')
    t0 = time.time()
    examples = extract_training_data(archive_dir, puzzle_dir=puzzle_dir)
    print(f'Extracted {len(examples)} examples in {time.time()-t0:.1f}s')

    if not examples:
        print('No training examples found!')
        return

    # Check how many have valid sum4 scores
    n_scored = sum(1 for ex in examples if ex.sum4_score > 0)
    has_scores = n_scored > 0
    print(f'  Examples with sum4 scores: {n_scored}/{len(examples)}')

    # Split train/val (90/10)
    dataset = TapeDataset(examples)
    val_size = max(1, len(dataset) // 10)
    train_size = len(dataset) - val_size
    train_ds, val_ds = random_split(
        dataset, [train_size, val_size],
        generator=torch.Generator().manual_seed(42))

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True,
                              num_workers=0, pin_memory=(device == 'cuda'))
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False,
                            num_workers=0, pin_memory=(device == 'cuda'))

    print(f'Train: {train_size}, Val: {val_size}')

    # Model
    model = TapeTransformer(
        d_model=128, n_heads=4, n_layers=4, d_ff=512, dropout=0.1,
        context_dim=CONTEXT_DIM,
    ).to(dev)

    n_params = sum(p.numel() for p in model.parameters())
    print(f'Model params: {n_params:,} (context_dim={CONTEXT_DIM})')

    # Optimizer + scheduler
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)

    total_steps = epochs * len(train_loader)
    warmup_steps = min(500, total_steps // 10)

    def lr_lambda(step):
        if step < warmup_steps:
            return step / max(1, warmup_steps)
        progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
        return 0.5 * (1 + torch.cos(torch.tensor(progress * 3.14159)).item())

    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)

    # Losses
    tape_criterion = nn.CrossEntropyLoss(ignore_index=PAD_TOKEN)
    score_criterion = nn.MSELoss()

    # Training loop
    best_val_loss = float('inf')
    stagnation = 0
    global_step = 0

    checkpoint_path = Path(checkpoint_dir) / 'tape_transformer.pt'

    print(f'\nTraining for {epochs} epochs (early stopping patience={patience})...')
    if has_scores:
        print(f'Multi-task: tape_CE + {score_weight} * score_MSE\n')
    else:
        print('Tape-only training (no sum4 scores available)\n')

    for epoch in range(epochs):
        # Train
        model.train()
        train_loss = 0.0
        train_tokens = 0
        train_score_loss = 0.0
        train_score_n = 0

        for context, tokens, sum4_scores in train_loader:
            context = context.to(dev)
            tokens = tokens.to(dev)
            sum4_scores = sum4_scores.to(dev)

            # Teacher forcing: input = tokens[:-1], target = tokens[1:]
            input_tokens = tokens[:, :-1]
            target_tokens = tokens[:, 1:]

            logits = model(context, input_tokens)

            # Tape loss
            tape_loss = tape_criterion(
                logits.reshape(-1, logits.size(-1)),
                target_tokens.reshape(-1),
            )

            # Score loss (only for examples with valid sum4)
            total_loss = tape_loss
            if has_scores:
                score_mask = sum4_scores > 0
                if score_mask.any():
                    pred_scores = model.predict_score(context)
                    score_loss = score_criterion(
                        pred_scores[score_mask],
                        sum4_scores[score_mask],
                    )
                    total_loss = tape_loss + score_weight * score_loss
                    train_score_loss += score_loss.item() * score_mask.sum().item()
                    train_score_n += score_mask.sum().item()

            optimizer.zero_grad()
            total_loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()

            n_toks = (target_tokens != PAD_TOKEN).sum().item()
            train_loss += tape_loss.item() * n_toks
            train_tokens += n_toks
            global_step += 1

        avg_train = train_loss / max(1, train_tokens)
        avg_score = train_score_loss / max(1, train_score_n) if train_score_n > 0 else 0

        # Validate
        model.eval()
        val_loss = 0.0
        val_tokens = 0

        with torch.no_grad():
            for context, tokens, sum4_scores in val_loader:
                context = context.to(dev)
                tokens = tokens.to(dev)

                input_tokens = tokens[:, :-1]
                target_tokens = tokens[:, 1:]

                logits = model(context, input_tokens)
                loss = tape_criterion(
                    logits.reshape(-1, logits.size(-1)),
                    target_tokens.reshape(-1),
                )
                n_toks = (target_tokens != PAD_TOKEN).sum().item()
                val_loss += loss.item() * n_toks
                val_tokens += n_toks

        avg_val = val_loss / max(1, val_tokens)

        # Early stopping
        if avg_val < best_val_loss:
            best_val_loss = avg_val
            stagnation = 0
            model.save(str(checkpoint_path))
        else:
            stagnation += 1

        if epoch % 10 == 0 or stagnation == 0:
            lr_now = optimizer.param_groups[0]['lr']
            score_str = f' score_mse={avg_score:.1f}' if train_score_n > 0 else ''
            print(f'Epoch {epoch:3d} | train_loss={avg_train:.4f}{score_str} | '
                  f'val_loss={avg_val:.4f} | lr={lr_now:.6f} | '
                  f'best_val={best_val_loss:.4f} | stag={stagnation}')

        if stagnation >= patience:
            print(f'\nEarly stopping at epoch {epoch} (patience={patience})')
            break

    print(f'\nTraining complete. Best val loss: {best_val_loss:.4f}')
    print(f'Checkpoint saved to: {checkpoint_path}')


def main():
    parser = argparse.ArgumentParser(description='Train TapeTransformer')
    parser.add_argument('--archive-dir', default='tools/om-archive')
    parser.add_argument('--puzzle-dir', default=None,
                        help='Directory with .puzzle files for puzzle-aware features')
    parser.add_argument('--epochs', type=int, default=200)
    parser.add_argument('--batch-size', type=int, default=64)
    parser.add_argument('--lr', type=float, default=3e-4)
    parser.add_argument('--device', default='cuda',
                        choices=['cpu', 'mps', 'cuda'])
    parser.add_argument('--checkpoint-dir', default='solver/checkpoints')
    parser.add_argument('--patience', type=int, default=20)
    parser.add_argument('--score-weight', type=float, default=0.1,
                        help='Weight for score prediction MSE loss')
    args = parser.parse_args()

    train(
        archive_dir=args.archive_dir,
        puzzle_dir=args.puzzle_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        device=args.device,
        checkpoint_dir=args.checkpoint_dir,
        patience=args.patience,
        score_weight=args.score_weight,
    )


if __name__ == '__main__':
    main()
