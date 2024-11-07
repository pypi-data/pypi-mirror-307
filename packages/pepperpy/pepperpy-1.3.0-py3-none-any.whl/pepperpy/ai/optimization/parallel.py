import math
from dataclasses import dataclass
from typing import Optional

import torch
import torch.distributed as dist
import torch.nn as nn


@dataclass
class ParallelConfig:
    """Configuration for tensor parallelism"""

    world_size: int = 1
    tp_size: int = 1  # Tensor parallel size
    pp_size: int = 1  # Pipeline parallel size
    chunk_size: int = 1
    overlap_comm: bool = True
    dtype: torch.dtype = torch.float16


class TensorParallel:
    """Tensor parallelism implementation"""

    def __init__(self, config: ParallelConfig):
        self.config = config

        # Initialize process groups
        if dist.is_initialized():
            self.rank = dist.get_rank()
            self.world_size = dist.get_world_size()

            # Create tensor parallel group
            ranks = list(range(config.tp_size))
            self.tp_group = dist.new_group(ranks)
            self.tp_rank = dist.get_rank(self.tp_group)
        else:
            self.rank = 0
            self.world_size = 1
            self.tp_group = None
            self.tp_rank = 0

    def split_tensor(self, tensor: torch.Tensor) -> torch.Tensor:
        """Split tensor across devices"""
        if self.tp_group is None:
            return tensor

        # Split last dimension
        chunk_size = tensor.size(-1) // self.config.tp_size
        return tensor[..., self.tp_rank * chunk_size : (self.tp_rank + 1) * chunk_size]

    def gather_tensor(self, tensor: torch.Tensor) -> torch.Tensor:
        """Gather tensor from devices"""
        if self.tp_group is None:
            return tensor

        # Gather along last dimension
        gathered = [torch.zeros_like(tensor) for _ in range(self.config.tp_size)]
        dist.all_gather(gathered, tensor, group=self.tp_group)
        return torch.cat(gathered, dim=-1)

    def parallel_matmul(
        self,
        input: torch.Tensor,
        weight: torch.Tensor,
        bias: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """Parallel matrix multiplication"""
        # Split weight matrix
        local_weight = self.split_tensor(weight)

        # Local computation
        local_output = torch.matmul(input, local_weight.t())

        # Add bias if present
        if bias is not None:
            local_bias = self.split_tensor(bias)
            local_output = local_output + local_bias

        # Gather results
        return self.gather_tensor(local_output)


class ParallelLinear(nn.Module):
    """Linear layer with tensor parallelism"""

    def __init__(
        self,
        in_features: int,
        out_features: int,
        bias: bool = True,
        parallel_config: ParallelConfig = None,
    ):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.parallel = TensorParallel(parallel_config or ParallelConfig())

        # Initialize parameters
        self.weight = nn.Parameter(
            torch.empty(out_features, in_features, dtype=self.parallel.config.dtype)
        )
        if bias:
            self.bias = nn.Parameter(torch.empty(out_features, dtype=self.parallel.config.dtype))
        else:
            self.register_parameter("bias", None)

        self.reset_parameters()

    def reset_parameters(self) -> None:
        """Initialize parameters"""
        nn.init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        if self.bias is not None:
            fan_in, _ = nn.init._calculate_fan_in_and_fan_out(self.weight)
            bound = 1 / math.sqrt(fan_in)
            nn.init.uniform_(self.bias, -bound, bound)

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        """Forward pass with parallel computation"""
        return self.parallel.parallel_matmul(input, self.weight, self.bias)
