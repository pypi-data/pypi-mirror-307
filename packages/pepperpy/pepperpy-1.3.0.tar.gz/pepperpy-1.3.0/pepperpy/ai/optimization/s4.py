from dataclasses import dataclass

import numpy as np
import torch
import torch.nn as nn


@dataclass
class S4Config:
    """Configuration for Structured State Space Model"""

    d_model: int = 256
    d_state: int = 64
    dropout: float = 0.1
    bidirectional: bool = True
    dt_min: float = 0.001
    dt_max: float = 0.1


class S4Layer(nn.Module):
    """Structured State Space Sequence Model Layer"""

    def __init__(self, config: S4Config):
        super().__init__()
        self.config = config

        # Initialize parameters
        self.A = nn.Parameter(torch.randn(config.d_state, config.d_state))
        self.B = nn.Parameter(torch.randn(config.d_state, 1))
        self.C = nn.Parameter(torch.randn(config.d_model, config.d_state))
        self.D = nn.Parameter(torch.randn(config.d_model, 1))

        # Initialize step sizes
        log_dt = torch.rand(1) * (np.log(config.dt_max) - np.log(config.dt_min))
        log_dt = log_dt + np.log(config.dt_min)
        self.log_dt = nn.Parameter(log_dt)

        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass with SSM computation"""
        batch, length, dim = x.shape
        dt = torch.exp(self.log_dt)

        # Compute state space model
        def ssm_forward(x_seq: torch.Tensor) -> torch.Tensor:
            u = x_seq.unsqueeze(-1)  # (batch, length, dim, 1)

            # Initialize state
            h = torch.zeros(batch, dim, self.config.d_state, device=x.device)

            # Step through sequence
            outputs = []
            for t in range(length):
                # Update state
                h = h + dt * (torch.matmul(h, self.A.T) + torch.matmul(u[:, t], self.B.T))

                # Compute output
                y = torch.matmul(h, self.C.T) + torch.matmul(u[:, t], self.D.T)
                outputs.append(y)

            return torch.stack(outputs, dim=1)

        # Forward and backward passes for bidirectional
        output = ssm_forward(x)
        if self.config.bidirectional:
            output_backward = ssm_forward(torch.flip(x, [1]))
            output = output + torch.flip(output_backward, [1])

        return self.dropout(output)


class S4Block(nn.Module):
    """S4 Block combining SSM with normalization and residual"""

    def __init__(self, config: S4Config):
        super().__init__()
        self.norm = nn.LayerNorm(config.d_model)
        self.s4 = S4Layer(config)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass with residual connection"""
        return x + self.s4(self.norm(x))


class S4Optimizer:
    """Optimizer for converting models to use S4"""

    @staticmethod
    def convert_to_s4(model: nn.Module, config: S4Config) -> nn.Module:
        """Convert attention layers to S4"""
        for name, module in model.named_children():
            if isinstance(module, nn.MultiheadAttention):
                # Replace attention with S4
                setattr(model, name, S4Block(config))
            elif len(list(module.children())) > 0:
                # Recurse for nested modules
                S4Optimizer.convert_to_s4(module, config)

        return model
