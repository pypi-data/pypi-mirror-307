from dataclasses import dataclass
from typing import Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as f


@dataclass
class SparseConfig:
    """Configuration for sparse inference"""

    sparsity: float = 0.9
    block_size: int = 16
    min_nonzero: int = 4
    pruning_method: str = "magnitude"


class BlockSparseLinear(nn.Module):
    """Block-sparse linear layer"""

    def __init__(self, in_features: int, out_features: int, config: SparseConfig):
        super().__init__()
        self.config = config
        self.in_features = in_features
        self.out_features = out_features

        # Initialize dense weights
        self.weight = nn.Parameter(torch.randn(out_features, in_features) / np.sqrt(in_features))
        self.bias = nn.Parameter(torch.zeros(out_features))

        # Initialize sparsity mask
        self.register_buffer("mask", torch.ones_like(self.weight, dtype=torch.bool))

    def update_mask(self) -> None:
        """Update sparsity mask"""
        with torch.no_grad():
            # Get block view of weights
            block_view = self.weight.view(-1, self.config.block_size, self.config.block_size)

            # Calculate block norms
            block_norms = torch.norm(block_view, dim=(1, 2))

            # Keep top-k blocks
            k = int((1 - self.config.sparsity) * len(block_norms))
            k = max(k, self.config.min_nonzero)
            threshold = torch.kthvalue(block_norms, k).values

            # Update mask
            block_mask = (block_norms > threshold).view(
                self.out_features // self.config.block_size,
                self.in_features // self.config.block_size,
            )
            self.mask = block_mask.repeat_interleave(
                self.config.block_size, dim=0
            ).repeat_interleave(self.config.block_size, dim=1)

    def to_sparse(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """Convert to sparse format"""
        indices = torch.nonzero(self.mask).t()
        values = self.weight[self.mask]
        return indices, values

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass with sparse computation"""
        # Apply mask
        sparse_weight = self.weight * self.mask

        # Compute output
        output = f.linear(x, sparse_weight, self.bias)
        return output


class SparseOptimizer:
    """Optimizer for sparse inference"""

    @staticmethod
    def convert_to_sparse(model: nn.Module, config: SparseConfig) -> nn.Module:
        """Convert linear layers to block-sparse"""
        for name, module in model.named_children():
            if isinstance(module, nn.Linear):
                # Replace with block-sparse layer
                sparse_layer = BlockSparseLinear(module.in_features, module.out_features, config)
                # Copy weights
                sparse_layer.weight.data.copy_(module.weight.data)
                sparse_layer.bias.data.copy_(module.bias.data)
                # Update sparsity mask
                sparse_layer.update_mask()
                setattr(model, name, sparse_layer)
            elif len(list(module.children())) > 0:
                # Recurse for nested modules
                SparseOptimizer.convert_to_sparse(module, config)

        return model
