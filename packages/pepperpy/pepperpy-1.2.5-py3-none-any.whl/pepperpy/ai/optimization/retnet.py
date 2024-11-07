from dataclasses import dataclass
from typing import Dict, Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class RetNetConfig:
    """Configuration for Retention Network"""

    d_model: int = 256
    n_heads: int = 4
    dropout: float = 0.1
    chunk_size: int = 128
    use_decay: bool = True
    decay_rate: float = 0.9


class MultiScaleRetention(nn.Module):
    """Multi-scale retention mechanism"""

    def __init__(self, config: RetNetConfig):
        super().__init__()
        self.config = config
        assert config.d_model % config.n_heads == 0

        self.d_head = config.d_model // config.n_heads
        self.scale = self.d_head**-0.5

        # Initialize projections
        self.q_proj = nn.Linear(config.d_model, config.d_model)
        self.k_proj = nn.Linear(config.d_model, config.d_model)
        self.v_proj = nn.Linear(config.d_model, config.d_model)
        self.o_proj = nn.Linear(config.d_model, config.d_model)

        # Initialize decay factors
        if config.use_decay:
            self.decay = nn.Parameter(torch.ones(config.n_heads, 1, 1) * config.decay_rate)

        self.dropout = nn.Dropout(config.dropout)

    def forward(
        self, x: torch.Tensor, state: Optional[Dict[str, torch.Tensor]] = None
    ) -> torch.Tensor:
        """Forward pass with retention mechanism"""
        batch, length, dim = x.shape

        # Project inputs
        q = self.q_proj(x).view(batch, length, self.config.n_heads, self.d_head)
        k = self.k_proj(x).view(batch, length, self.config.n_heads, self.d_head)
        v = self.v_proj(x).view(batch, length, self.config.n_heads, self.d_head)

        # Compute retention
        def compute_chunk(
            q_chunk: torch.Tensor,
            k_chunk: torch.Tensor,
            v_chunk: torch.Tensor,
            chunk_state: Optional[Dict[str, torch.Tensor]] = None,
        ) -> torch.Tensor:
            chunk_length = q_chunk.size(1)

            # Initialize or get previous state
            if chunk_state is None:
                prev_k = torch.zeros_like(k_chunk[:, :1])
                prev_v = torch.zeros_like(v_chunk[:, :1])
            else:
                prev_k = chunk_state["k"]
                prev_v = chunk_state["v"]

            # Concatenate previous state with current chunk
            k_chunk = torch.cat([prev_k, k_chunk], dim=1)
            v_chunk = torch.cat([prev_v, v_chunk], dim=1)

            # Compute attention scores
            scores = torch.matmul(q_chunk, k_chunk.transpose(-2, -1)) * self.scale

            # Apply decay if enabled
            if self.config.use_decay:
                position_ids = torch.arange(chunk_length, device=x.device).view(1, -1, 1, 1)
                scores = scores * (self.decay**position_ids)

            # Apply attention
            attn = F.softmax(scores, dim=-1)
            attn = self.dropout(attn)

            # Compute output
            output = torch.matmul(attn, v_chunk)

            # Update state
            new_state = {"k": k_chunk[:, -1:].detach(), "v": v_chunk[:, -1:].detach()}

            return output, new_state

        # Process in chunks
        outputs = []
        current_state = state

        for i in range(0, length, self.config.chunk_size):
            chunk_end = min(i + self.config.chunk_size, length)
            output_chunk, current_state = compute_chunk(
                q[:, i:chunk_end], k[:, i:chunk_end], v[:, i:chunk_end], current_state
            )
            outputs.append(output_chunk)

        output = torch.cat(outputs, dim=1)
        output = output.reshape(batch, length, dim)

        return self.o_proj(output)


class RetNetBlock(nn.Module):
    """RetNet block with normalization and residual"""

    def __init__(self, config: RetNetConfig):
        super().__init__()
        self.norm = nn.LayerNorm(config.d_model)
        self.retention = MultiScaleRetention(config)

    def forward(
        self, x: torch.Tensor, state: Optional[Dict[str, torch.Tensor]] = None
    ) -> torch.Tensor:
        """Forward pass with residual connection"""
        return x + self.retention(self.norm(x), state)


class RetNetOptimizer:
    """Optimizer for converting models to use RetNet"""

    @staticmethod
    def convert_to_retnet(model: nn.Module, config: RetNetConfig) -> nn.Module:
        """Convert attention layers to RetNet"""
        for name, module in model.named_children():
            if isinstance(module, nn.MultiheadAttention):
                # Replace attention with RetNet
                setattr(model, name, RetNetBlock(config))
            elif len(list(module.children())) > 0:
                # Recurse for nested modules
                RetNetOptimizer.convert_to_retnet(module, config)

        return model
