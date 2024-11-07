from abc import ABC, abstractmethod
from typing import List

import numpy as np

from pepperpy.core.exceptions import DependencyError


class EmbeddingProvider(ABC):
    """Base class for embedding providers"""

    @abstractmethod
    async def embed_text(self, text: str) -> np.ndarray:
        """Generate embeddings for text"""
        pass

    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for multiple texts"""
        pass

    async def similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        emb1 = await self.embed_text(text1)
        emb2 = await self.embed_text(text2)
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))


class LocalEmbedding(EmbeddingProvider):
    """Local embedding provider using sentence-transformers"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        try:
            from sentence_transformers import SentenceTransformer

            self.model = SentenceTransformer(model_name)
        except ImportError as err:
            raise DependencyError(
                "sentence-transformers not installed. "
                "Install with: pip install sentence-transformers"
            ) from err

    async def embed_text(self, text: str) -> np.ndarray:
        """Generate embeddings using local model"""
        return self.model.encode(text)

    async def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for multiple texts"""
        return self.model.encode(texts)
