from typing import Any, Dict

import torch
import torch.nn.utils.prune as prune
from neural_compressor import quantization
from neural_compressor.config import PostTrainingQuantConfig
from optimum.onnx import OnnxConfig
from transformers import AutoModelForCausalLM


class ModelCompressor:
    """Model compression and pruning utilities"""

    @staticmethod
    async def prune_model(
        model: AutoModelForCausalLM,
        amount: float = 0.3,
        method: str = "l1_unstructured",
    ) -> AutoModelForCausalLM:
        """Prune model weights"""
        for _, module in model.named_modules():
            if isinstance(module, torch.nn.Linear):
                if method == "l1_unstructured":
                    prune.l1_unstructured(module, "weight", amount=amount)
                elif method == "random_unstructured":
                    prune.random_unstructured(module, "weight", amount=amount)

        return model

    @staticmethod
    async def quantize_dynamic(
        model: AutoModelForCausalLM, dtype: str = "int8"
    ) -> AutoModelForCausalLM:
        """Dynamic quantization"""
        return torch.quantization.quantize_dynamic(
            model, {torch.nn.Linear}, dtype=getattr(torch, dtype)
        )

    @staticmethod
    async def export_onnx(
        model: AutoModelForCausalLM, save_path: str, input_shape: Dict[str, Any]
    ) -> None:
        """Export to ONNX format"""
        onnx_config = OnnxConfig.from_model_config(model.config)
        _ = onnx_config.export(
            model=model, output_path=save_path, input_shape=input_shape, opset=13
        )

    @staticmethod
    async def optimize_onnx(model_path: str, save_path: str, dtype: str = "int8") -> None:
        """Optimize ONNX model"""
        conf = PostTrainingQuantConfig(backend="onnxruntime", approach="dynamic", precision=dtype)
        quantizer = quantization.Quantization(conf)
        quantizer.model = model_path
        quantizer.calib_dataloader = None
        quantizer.eval_func = None
        quantized_model = quantizer.fit()
        quantized_model.save(save_path)
