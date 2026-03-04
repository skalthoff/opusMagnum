"""TapeTransformer: decoder-only transformer for tape generation.

Conditioned on layout features via a CLS prefix token.
Generates instruction sequences autoregressively.
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn

from .dl_data import VOCAB_SIZE, CONTEXT_DIM, LAYOUT_DIM, MAX_SEQ_LEN, PAD_TOKEN


class PositionalEncoding(nn.Module):
    """Sinusoidal positional encoding."""

    def __init__(self, d_model: int, max_len: int = MAX_SEQ_LEN + 1):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe.unsqueeze(0))  # [1, max_len, d_model]

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.pe[:, :x.size(1)]


class TapeTransformer(nn.Module):
    """Decoder-only transformer for tape generation.

    Architecture:
        Layout features [CONTEXT_DIM] -> LayoutEncoder -> CLS token [1, d_model]
        Target tokens -> TokenEmbedding + PosEncoding -> [seq_len, d_model]
        Prepend CLS -> causal self-attention -> Linear -> logits [seq_len, vocab]
    """

    def __init__(
        self,
        d_model: int = 128,
        n_heads: int = 4,
        n_layers: int = 4,
        d_ff: int = 512,
        dropout: float = 0.1,
        vocab_size: int = VOCAB_SIZE,
        context_dim: int = CONTEXT_DIM,
        max_seq_len: int = MAX_SEQ_LEN,
    ):
        super().__init__()
        self.d_model = d_model
        self.max_seq_len = max_seq_len
        self.vocab_size = vocab_size

        # Layout encoder: project context vector to CLS embedding
        self.layout_encoder = nn.Sequential(
            nn.Linear(context_dim, d_model),
            nn.ReLU(),
            nn.Linear(d_model, d_model),
        )

        # Token embedding + positional encoding
        self.token_embedding = nn.Embedding(vocab_size, d_model, padding_idx=PAD_TOKEN)
        self.pos_encoding = PositionalEncoding(d_model, max_seq_len + 1)
        self.dropout = nn.Dropout(dropout)

        # Transformer decoder layers
        decoder_layer = nn.TransformerDecoderLayer(
            d_model=d_model,
            nhead=n_heads,
            dim_feedforward=d_ff,
            dropout=dropout,
            batch_first=True,
        )
        self.decoder = nn.TransformerDecoder(decoder_layer, num_layers=n_layers)

        # Output head (tape tokens)
        self.output_head = nn.Linear(d_model, vocab_size)

        # Score head: predict sum4 from CLS embedding
        self.score_head = nn.Sequential(
            nn.Linear(d_model, d_model),
            nn.ReLU(),
            nn.Linear(d_model, 1),
        )

        # Store context_dim for checkpoint compat
        self.context_dim = context_dim

        # Initialize weights
        self._init_weights()

    def _init_weights(self):
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)

    def forward(
        self,
        context: torch.Tensor,      # [batch, CONTEXT_DIM]
        target_tokens: torch.Tensor, # [batch, seq_len] token IDs
    ) -> torch.Tensor:
        """Forward pass with teacher forcing.

        Returns logits [batch, seq_len, vocab_size] for next-token prediction.
        """
        batch_size, seq_len = target_tokens.shape

        # Encode layout context into CLS embedding
        cls_emb = self.layout_encoder(context).unsqueeze(1)  # [B, 1, d_model]

        # Embed target tokens
        tok_emb = self.token_embedding(target_tokens)  # [B, seq_len, d_model]

        # Concatenate CLS + token embeddings
        combined = torch.cat([cls_emb, tok_emb], dim=1)  # [B, 1+seq_len, d_model]
        combined = self.pos_encoding(combined)
        combined = self.dropout(combined)

        # Causal mask (prevent attending to future tokens)
        total_len = 1 + seq_len
        causal_mask = nn.Transformer.generate_square_subsequent_mask(
            total_len, device=context.device)

        # Self-attention (decoder-only: memory is not used, pass dummy)
        # We use TransformerDecoder but pass the same sequence as both tgt and memory
        # with a causal mask to get autoregressive behavior
        dummy_memory = torch.zeros(batch_size, 1, self.d_model, device=context.device)
        out = self.decoder(
            tgt=combined,
            memory=dummy_memory,
            tgt_mask=causal_mask,
        )

        # Take only the token positions (skip CLS)
        out = out[:, 1:, :]  # [B, seq_len, d_model]

        # Project to vocabulary
        logits = self.output_head(out)  # [B, seq_len, vocab_size]
        return logits

    def predict_score(
        self,
        context: torch.Tensor,      # [batch, CONTEXT_DIM]
    ) -> torch.Tensor:
        """Predict sum4 score from layout+puzzle context.

        Returns [batch] tensor of predicted sum4 values.
        """
        cls = self.layout_encoder(context)  # [B, d_model]
        return self.score_head(cls).squeeze(-1)  # [B]

    def generate_step(
        self,
        context: torch.Tensor,      # [batch, CONTEXT_DIM]
        tokens_so_far: torch.Tensor, # [batch, current_len] token IDs
    ) -> torch.Tensor:
        """Generate logits for the next token given context and tokens so far.

        Returns logits [batch, vocab_size] for the next position.
        """
        logits = self.forward(context, tokens_so_far)
        return logits[:, -1, :]  # [batch, vocab_size]

    def save(self, path: str):
        """Save model checkpoint."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        torch.save({
            'model_state_dict': self.state_dict(),
            'd_model': self.d_model,
            'vocab_size': self.vocab_size,
            'max_seq_len': self.max_seq_len,
            'context_dim': self.context_dim,
        }, path)

    @classmethod
    def load(cls, path: str, device: str = 'cpu') -> 'TapeTransformer':
        """Load model from checkpoint."""
        checkpoint = torch.load(path, map_location=device, weights_only=True)
        model = cls(
            d_model=checkpoint.get('d_model', 128),
            vocab_size=checkpoint.get('vocab_size', VOCAB_SIZE),
            max_seq_len=checkpoint.get('max_seq_len', MAX_SEQ_LEN),
            context_dim=checkpoint.get('context_dim', LAYOUT_DIM),
        )
        # Handle loading old checkpoints (120-dim) into new model (164-dim)
        state = checkpoint['model_state_dict']
        saved_ctx = checkpoint.get('context_dim', LAYOUT_DIM)
        if saved_ctx != model.context_dim:
            # Resize layout_encoder.0.weight: [d_model, old_dim] → [d_model, new_dim]
            old_w = state['layout_encoder.0.weight']
            old_b = state['layout_encoder.0.bias']
            new_w = torch.zeros(model.d_model, model.context_dim)
            new_w[:, :old_w.shape[1]] = old_w
            state['layout_encoder.0.weight'] = new_w
            state['layout_encoder.0.bias'] = old_b
        model.load_state_dict(state, strict=False)
        model.eval()
        return model
