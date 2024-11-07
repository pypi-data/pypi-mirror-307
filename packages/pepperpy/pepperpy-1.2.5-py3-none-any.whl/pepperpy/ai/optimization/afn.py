from dataclasses import dataclass

import torch
import torch.nn as nn
from transformers import PreTrainedModel


@dataclass
class AFNConfig:
    """Configuration for Attention Free Network optimization"""

    hidden_size: int = 768
    intermediate_size: int = 3072
    num_hidden_layers: int = 12
    chunk_size: int = 128


class AFNOptimizer:
    """Optimize models using Attention Free Networks"""

    @staticmethod
    async def convert_to_afn(model: PreTrainedModel, config: AFNConfig) -> PreTrainedModel:
        """Convert transformer model to AFN architecture"""
        # Replace self-attention with AFN blocks
        for layer in model.encoder.layer:
            # Create AFN block
            afn_block = nn.Sequential(
                nn.Linear(config.hidden_size, config.intermediate_size),
                nn.GELU(),
                nn.Linear(config.intermediate_size, config.hidden_size),
            )

            # Replace attention with AFN
            layer.attention = afn_block

        return model

    @staticmethod
    async def optimize_memory_access(model: PreTrainedModel, config: AFNConfig) -> PreTrainedModel:
        """Optimize memory access patterns"""

        def chunk_and_pad(tensor: torch.Tensor) -> torch.Tensor:
            # Chunk input for efficient processing
            chunks = tensor.split(config.chunk_size, dim=1)
            if len(chunks[-1]) < config.chunk_size:
                pad_size = config.chunk_size - len(chunks[-1])
                chunks = chunks[:-1] + (torch.nn.functional.pad(chunks[-1], (0, pad_size)),)
            return torch.cat(chunks, dim=1)

        # Add chunking to forward pass
        original_forward = model.forward

        def chunked_forward(*args, **kwargs):
            # Apply chunking to input embeddings
            if "input_ids" in kwargs:
                kwargs["input_ids"] = chunk_and_pad(kwargs["input_ids"])
            return original_forward(*args, **kwargs)

        model.forward = chunked_forward
        return model
