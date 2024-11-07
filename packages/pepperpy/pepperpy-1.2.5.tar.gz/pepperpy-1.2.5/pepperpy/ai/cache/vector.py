from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import faiss
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


@dataclass
class VectorCacheConfig:
    """Configuration for vector cache"""

    engine: str = "faiss"  # or "qdrant"
    dimension: int = 768
    distance: str = "cosine"
    collection: str = "cache"
    url: Optional[str] = None


class VectorCache:
    """Vector-based caching using FAISS or Qdrant"""

    def __init__(self, config: VectorCacheConfig):
        self.config = config

        if config.engine == "faiss":
            self._init_faiss()
        else:
            self._init_qdrant()

    def _init_faiss(self):
        """Initialize FAISS index"""
        self.index = faiss.IndexFlatIP(self.config.dimension)
        self.vectors = []
        self.metadata = []

    def _init_qdrant(self):
        """Initialize Qdrant client"""
        self.client = QdrantClient(url=self.config.url)

        # Create collection if needed
        self.client.recreate_collection(
            collection_name=self.config.collection,
            vectors_config=VectorParams(size=self.config.dimension, distance=Distance.COSINE),
        )

    async def add(self, vector: np.ndarray, metadata: Dict[str, Any]) -> None:
        """Add vector to cache"""
        if self.config.engine == "faiss":
            self.index.add(vector.reshape(1, -1))
            self.vectors.append(vector)
            self.metadata.append(metadata)
        else:
            self.client.upsert(
                collection_name=self.config.collection,
                points=[
                    {
                        "id": len(self.metadata),
                        "vector": vector.tolist(),
                        "payload": metadata,
                    }
                ],
            )

    async def search(self, query: np.ndarray, k: int = 1) -> List[Dict[str, Any]]:
        """Search for similar vectors"""
        if self.config.engine == "faiss":
            _, indices = self.index.search(query.reshape(1, -1), k)
            return [self.metadata[i] for i in indices[0]]
        else:
            results = self.client.search(
                collection_name=self.config.collection,
                query_vector=query.tolist(),
                limit=k,
            )
            return [hit.payload for hit in results]
