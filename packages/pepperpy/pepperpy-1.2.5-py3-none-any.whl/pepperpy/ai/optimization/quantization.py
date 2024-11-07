from typing import Dict, Optional

from accelerate import load_checkpoint_and_dispatch
from auto_gptq import AutoGPTQForCausalLM
from transformers import AutoModelForCausalLM


class ModelOptimizer:
    """Model optimization and quantization"""

    @staticmethod
    async def quantize_model(
        model_id: str, bits: int = 4, group_size: int = 128, device: str = "cuda:0"
    ) -> AutoModelForCausalLM:
        """Quantize model to reduced precision"""
        if bits == 4:
            # Use GPTQ for 4-bit quantization
            model = AutoGPTQForCausalLM.from_pretrained(
                model_id,
                quantize_config={
                    "bits": bits,
                    "group_size": group_size,
                    "desc_act": True,
                },
            )
        else:
            # Use bitsandbytes for 8-bit quantization
            model = AutoModelForCausalLM.from_pretrained(
                model_id, load_in_8bit=True, device_map="auto"
            )

        return model

    @staticmethod
    async def optimize_memory(
        model: AutoModelForCausalLM,
        device_map: Optional[Dict[str, str]] = None,
        max_memory: Optional[Dict[int, str]] = None,
    ) -> AutoModelForCausalLM:
        """Optimize model memory usage"""
        # Use accelerate for device mapping
        model = load_checkpoint_and_dispatch(
            model,
            device_map=device_map or "auto",
            max_memory=max_memory,
            no_split_module_classes=["GPTBlock"],
        )

        return model
