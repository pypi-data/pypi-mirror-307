from dataclasses import dataclass

import bitsandbytes as bnb
import torch
import torch.nn as nn
from transformers import PreTrainedModel


@dataclass
class QuantConfig:
    """Configuration for quantization"""

    bits: int = 4
    group_size: int = 128
    double_quant: bool = True
    use_cuda: bool = True


class QuantizedInference:
    """Optimized quantized inference"""

    def __init__(self, config: QuantConfig):
        self.config = config

    def quantize_model(self, model: PreTrainedModel, dtype: str = "int8") -> PreTrainedModel:
        """Quantize model weights"""
        if self.config.bits == 4:
            return self._quantize_4bit(model)
        else:
            return self._quantize_8bit(model)

    def _quantize_4bit(self, model: PreTrainedModel) -> PreTrainedModel:
        """4-bit quantization with double quantization"""
        for name, module in model.named_modules():
            if isinstance(module, nn.Linear):
                # Replace with 4-bit quantized module
                quantized = bnb.nn.Linear4Bit(
                    module.in_features,
                    module.out_features,
                    bias=module.bias is not None,
                    compute_dtype=torch.float16 if self.config.use_cuda else torch.float32,
                    compress_statistics=self.config.double_quant,
                    quant_type="nf4",  # Normal Float 4
                )
                # Copy weights
                quantized.weight = module.weight
                if module.bias is not None:
                    quantized.bias = module.bias

                # Replace module
                parent_name = name.rsplit(".", 1)[0]
                parent = model.get_submodule(parent_name)
                child_name = name.rsplit(".", 1)[1]
                setattr(parent, child_name, quantized)

        return model

    def _quantize_8bit(self, model: PreTrainedModel) -> PreTrainedModel:
        """8-bit quantization"""
        for name, module in model.named_modules():
            if isinstance(module, nn.Linear):
                # Replace with 8-bit quantized module
                quantized = bnb.nn.Linear8Bit(
                    module.in_features,
                    module.out_features,
                    bias=module.bias is not None,
                    has_fp16_weights=self.config.use_cuda,
                    threshold=6.0,
                )
                # Copy weights
                quantized.weight = module.weight
                if module.bias is not None:
                    quantized.bias = module.bias

                # Replace module
                parent_name = name.rsplit(".", 1)[0]
                parent = model.get_submodule(parent_name)
                child_name = name.rsplit(".", 1)[1]
                setattr(parent, child_name, quantized)

        return model
