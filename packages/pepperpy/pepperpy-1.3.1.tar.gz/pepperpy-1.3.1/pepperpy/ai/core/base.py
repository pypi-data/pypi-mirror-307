from abc import ABC, abstractmethod
from typing import Any, Dict, Protocol

import numpy as np
import torch


class AIProvider(Protocol):
    """Base protocol for AI providers"""

    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt"""
        ...

    async def embed(self, text: str) -> np.ndarray:
        """Generate embeddings"""
        ...

    @property
    def device(self) -> torch.device:
        """Get provider device"""
        ...


class AIModel(ABC):
    """Base class for AI models"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._initialized = False

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize model resources"""
        self._initialized = True

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup model resources"""
        self._initialized = False

    @property
    def device(self) -> torch.device:
        return self._device

    @property
    def initialized(self) -> bool:
        return self._initialized
