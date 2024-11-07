from dataclasses import dataclass

import numpy as np
from llama_cpp import Llama


@dataclass
class GGMLConfig:
    """Configuration for GGML models"""

    model_path: str
    n_ctx: int = 2048
    n_threads: int = 4
    n_gpu_layers: int = 0
    use_mmap: bool = True
    use_mlock: bool = False
    vocab_only: bool = False


class GGMLModel:
    """Efficient CPU inference using GGML/GGUF format"""

    def __init__(self, config: GGMLConfig):
        self.config = config
        self.model = Llama(
            model_path=config.model_path,
            n_ctx=config.n_ctx,
            n_threads=config.n_threads,
            n_gpu_layers=config.n_gpu_layers,
            use_mmap=config.use_mmap,
            use_mlock=config.use_mlock,
            vocab_only=config.vocab_only,
        )

    async def generate(
        self,
        prompt: str,
        max_tokens: int = 128,
        temperature: float = 0.7,
        top_p: float = 0.95,
        **kwargs,
    ) -> str:
        """Generate text efficiently on CPU"""
        output = self.model(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            **kwargs,
        )
        return output["choices"][0]["text"]

    async def embed(self, text: str) -> np.ndarray:
        """Generate embeddings efficiently"""
        return self.model.embed(text)
