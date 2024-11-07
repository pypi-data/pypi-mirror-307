from dataclasses import dataclass

import torch
import torch.nn as nn


@dataclass
class ActivationQuantConfig:
    """Configuration for activation quantization"""

    bits: int = 8
    symmetric: bool = True
    per_channel: bool = True
    calibration_size: int = 128
    percentile: float = 99.9


class ActivationQuantizer(nn.Module):
    """Quantizer for activations with calibration"""

    def __init__(self, config: ActivationQuantConfig):
        super().__init__()
        self.config = config
        self.register_buffer("scale", None)
        self.register_buffer("zero_point", None)
        self.calibrated = False

    def calibrate(self, x: torch.Tensor) -> None:
        """Calibrate quantization parameters"""
        if self.config.per_channel:
            dims = [0, 2, 3] if len(x.shape) == 4 else [0]
            values = torch.abs(x).permute(1, *range(len(dims))).reshape(x.size(1), -1)
        else:
            values = x.abs().reshape(-1)

        # Calculate scale using percentile
        max_val = torch.quantile(values, self.config.percentile / 100, dim=-1)

        if self.config.symmetric:
            self.scale = max_val / (2 ** (self.config.bits - 1) - 1)
            self.zero_point = torch.zeros_like(self.scale)
        else:
            min_val = values.min(dim=-1).values
            self.scale = (max_val - min_val) / (2**self.config.bits - 1)
            self.zero_point = min_val

        self.calibrated = True

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Quantize activations"""
        if not self.calibrated:
            self.calibrate(x)

        # Quantize
        x_scaled = x / self.scale
        x_clipped = x_scaled.clamp(-(2 ** (self.config.bits - 1)), 2 ** (self.config.bits - 1) - 1)
        x_rounded = torch.round(x_clipped)

        # Dequantize
        x_dequant = x_rounded * self.scale
        return x_dequant


class ActivationQuantOptimizer:
    """Optimizer for activation quantization"""

    @staticmethod
    def add_activation_quantization(model: nn.Module, config: ActivationQuantConfig) -> nn.Module:
        """Add activation quantization to model"""
        for name, module in model.named_children():
            if isinstance(module, (nn.ReLU, nn.GELU, nn.SiLU)):
                # Add quantizer after activation
                setattr(model, name, nn.Sequential(module, ActivationQuantizer(config)))
            elif len(list(module.children())) > 0:
                # Recurse for nested modules
                ActivationQuantOptimizer.add_activation_quantization(module, config)

        return model
