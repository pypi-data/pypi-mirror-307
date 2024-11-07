from abc import ABC, abstractmethod
from typing import Dict, Optional

import torch
from accelerate import load_checkpoint_and_dispatch
from optimum.bettertransformer import BetterTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer


class LLMConfig:
    """Configuration for LLM models"""

    model_id: str
    device_map: str = "auto"
    torch_dtype: torch.dtype = torch.float16
    load_in_8bit: bool = False
    use_better_transformer: bool = True
    max_memory: Optional[Dict[int, str]] = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class LLMBase(ABC):
    """Base class for LLM implementations"""

    @abstractmethod
    async def generate(
        self, prompt: str, max_length: int = 2048, temperature: float = 0.7, **kwargs
    ) -> str:
        """Generate text from prompt"""
        pass

    @abstractmethod
    async def embed(self, text: str) -> torch.Tensor:
        """Generate embeddings for text"""
        pass


class OptimizedLLM(LLMBase):
    """Optimized LLM implementation using best practices"""

    def __init__(self, config: LLMConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.model_id)

        # Load model with optimizations
        model = AutoModelForCausalLM.from_pretrained(
            config.model_id,
            device_map=config.device_map,
            torch_dtype=config.torch_dtype,
            load_in_8bit=config.load_in_8bit,
        )

        # Apply BetterTransformer optimizations
        if config.use_better_transformer:
            model = BetterTransformer.transform(model)

        # Load model across devices if needed
        if config.max_memory:
            model = load_checkpoint_and_dispatch(
                model,
                config.model_id,
                device_map="auto",
                max_memory=config.max_memory,
                no_split_module_classes=["GPTBlock"],
            )

        self.model = model

    async def generate(
        self, prompt: str, max_length: int = 2048, temperature: float = 0.7, **kwargs
    ) -> str:
        """Generate optimized text"""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs, max_length=max_length, temperature=temperature, **kwargs
            )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    async def embed(self, text: str) -> torch.Tensor:
        """Generate optimized embeddings"""
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(
            self.model.device
        )

        with torch.inference_mode():
            outputs = self.model.get_input_embeddings()(inputs.input_ids)
            # Get CLS token embedding or average
            embeddings = outputs.mean(dim=1)

        return embeddings
