"""Training script for TapeTransformer.

Usage:
    uv run python -m solver.dl_train --archive-dir tools/om-archive --epochs 200 --device mps
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
    epochs: int = 200,
    batch_size: int = 64,
    lr: float = 3e-4,
    device: str = 'mps',
    checkpoint_dir: str = 'solver/checkpoints',
    patience: int = 20,
):
    """Train the TapeTransformer on archive solutions."""
    import sys

    # Device setup
    if device == 'mps' and not torch.backends.mps.is_available():
        print('MPS not available, falling back to CPU', flush=True)
        device = 'cpu'
    dev = torch.device(device)
    print(f'Device: {dev}', flush=True)

    # Extract training data
    print(f'Extracting training data from {archive_dir}...')
    t0 = time.time()
    examples = extract_training_data(archive_dir)
    print(f'Extracted {len(examples)} examples in {time.time()-t0:.1f}s')

    if not examples:
        print('No training examples found!')
        return

    # Split train/val (90/10)
    dataset = TapeDataset(examples)
    val_size = max(1, len(dataset) // 10)
    train_size = len(dataset) - val_size
    train_ds, val_ds = random_split(
        dataset, [train_size, val_size],
        generator=torch.Generator().manual_seed(42))

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True,
                              num_workers=0, pin_memory=False)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False,
                            num_workers=0, pin_memory=False)

    print(f'Train: {train_size}, Val: {val_size}')

    # Model
    model = TapeTransformer(
        d_model=128, n_heads=4, n_layers=4, d_ff=512, dropout=0.1,
    ).to(dev)

    n_params = sum(p.numel() for p in model.parameters())
    print(f'Model params: {n_params:,}')

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

    # Loss
    criterion = nn.CrossEntropyLoss(ignore_index=PAD_TOKEN)

    # Training loop
    best_val_loss = float('inf')
    stagnation = 0
    global_step = 0

    checkpoint_path = Path(checkpoint_dir) / 'tape_transformer.pt'

    print(f'\nTraining for {epochs} epochs (early stopping patience={patience})...\n')

    for epoch in range(epochs):
        # Train
        model.train()
        train_loss = 0.0
        train_tokens = 0

        for context, tokens in train_loader:
            context = context.to(dev)
            tokens = tokens.to(dev)

            # Teacher forcing: input = tokens[:-1], target = tokens[1:]
            input_tokens = tokens[:, :-1]
            target_tokens = tokens[:, 1:]

            logits = model(context, input_tokens)

            # Reshape for cross-entropy: [B*seq_len, vocab] vs [B*seq_len]
            loss = criterion(
                logits.reshape(-1, logits.size(-1)),
                target_tokens.reshape(-1),
            )

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()

            n_toks = (target_tokens != PAD_TOKEN).sum().item()
            train_loss += loss.item() * n_toks
            train_tokens += n_toks
            global_step += 1

        avg_train = train_loss / max(1, train_tokens)

        # Validate
        model.eval()
        val_loss = 0.0
        val_tokens = 0

        with torch.no_grad():
            for context, tokens in val_loader:
                context = context.to(dev)
                tokens = tokens.to(dev)

                input_tokens = tokens[:, :-1]
                target_tokens = tokens[:, 1:]

                logits = model(context, input_tokens)
                loss = criterion(
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
            print(f'Epoch {epoch:3d} | train_loss={avg_train:.4f} | '
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
    parser.add_argument('--epochs', type=int, default=200)
    parser.add_argument('--batch-size', type=int, default=64)
    parser.add_argument('--lr', type=float, default=3e-4)
    parser.add_argument('--device', default='mps',
                        choices=['cpu', 'mps', 'cuda'])
    parser.add_argument('--checkpoint-dir', default='solver/checkpoints')
    parser.add_argument('--patience', type=int, default=20)
    args = parser.parse_args()

    train(
        archive_dir=args.archive_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        device=args.device,
        checkpoint_dir=args.checkpoint_dir,
        patience=args.patience,
    )


if __name__ == '__main__':
    main()
