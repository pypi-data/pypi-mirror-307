import math
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class HyenaConfig:
    """Configuration for Hyena operator"""

    d_model: int = 256
    max_length: int = 2048
    num_heads: int = 4
    dropout: float = 0.1
    activation: str = "silu"
    use_bias: bool = True


class HyenaOperator(nn.Module):
    """Hyena operator for efficient sequence modeling"""

    def __init__(self, config: HyenaConfig):
        super().__init__()
        self.config = config

        # Initialize filters
        self.filter_order = int(math.log2(config.max_length))
        self.filters = nn.ModuleList(
            [
                nn.Conv1d(
                    config.d_model,
                    config.d_model,
                    kernel_size=2**i,
                    padding=2 ** (i - 1),
                    groups=config.num_heads,
                )
                for i in range(self.filter_order)
            ]
        )

        # Initialize projections
        self.input_proj = nn.Linear(config.d_model, config.d_model)
        self.output_proj = nn.Linear(config.d_model, config.d_model)

        # Initialize gating
        self.gate = nn.Linear(config.d_model, config.d_model)

        self.dropout = nn.Dropout(config.dropout)
        self.activation = getattr(F, config.activation)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass with multi-scale filtering"""
        batch, length, dim = x.shape

        # Project input
        x = self.input_proj(x)
        x = x.transpose(1, 2)  # (batch, dim, length)

        # Apply multi-scale filters
        outputs = []
        for filter_layer in self.filters:
            filtered = filter_layer(x)
            outputs.append(filtered)

        # Combine filtered outputs
        combined = sum(outputs) / math.sqrt(self.filter_order)
        combined = combined.transpose(1, 2)  # (batch, length, dim)

        # Apply gating
        gate = self.activation(self.gate(x.transpose(1, 2)))
        output = combined * gate

        # Project output
        output = self.output_proj(output)
        return self.dropout(output)


class HyenaBlock(nn.Module):
    """Hyena block with normalization and residual"""

    def __init__(self, config: HyenaConfig):
        super().__init__()
        self.norm = nn.LayerNorm(config.d_model)
        self.hyena = HyenaOperator(config)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass with residual connection"""
        return x + self.hyena(self.norm(x))


class HyenaOptimizer:
    """Optimizer for converting models to use Hyena"""

    @staticmethod
    def convert_to_hyena(model: nn.Module, config: HyenaConfig) -> nn.Module:
        """Convert attention layers to Hyena"""
        for name, module in model.named_children():
            if isinstance(module, nn.MultiheadAttention):
                # Replace attention with Hyena
                setattr(model, name, HyenaBlock(config))
            elif len(list(module.children())) > 0:
                # Recurse for nested modules
                HyenaOptimizer.convert_to_hyena(module, config)

        return model
