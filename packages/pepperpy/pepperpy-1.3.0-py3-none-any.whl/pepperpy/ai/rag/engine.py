from dataclasses import dataclass
from typing import Any, Dict, List

import numpy as np

from ..embeddings.base import EmbeddingProvider
from ..text.chunking import ChunkingStrategy, TextChunk


@dataclass
class RAGConfig:
    """Configuration for RAG engine"""

    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 3
    similarity_threshold: float = 0.7
    rerank_top_k: int = 10
    use_mmr: bool = True  # Maximum Marginal Relevance
    mmr_lambda: float = 0.7


class RAGEngine:
    """Retrieval Augmented Generation engine"""

    def __init__(self, chunker: ChunkingStrategy, embedder: EmbeddingProvider, config: RAGConfig):
        self.chunker = chunker
        self.embedder = embedder
        self.config = config

    async def process_document(self, document: str, query: str) -> Dict[str, Any]:
        """Process document and retrieve relevant context"""
        # Split into chunks
        chunks = self.chunker.split(document, max_chunk_size=self.config.chunk_size)

        # Get embeddings
        chunk_embeddings = await self.embedder.embed_batch([chunk.content for chunk in chunks])
        query_embedding = await self.embedder.embed_text(query)

        # Get initial top-k chunks
        if self.config.use_mmr:
            selected_chunks = await self._mmr_selection(query_embedding, chunks, chunk_embeddings)
        else:
            selected_chunks = await self._similarity_selection(
                query_embedding, chunks, chunk_embeddings
            )

        return {
            "chunks": selected_chunks,
            "context": "\n\n".join(chunk.content for chunk in selected_chunks),
        }

    async def _mmr_selection(
        self,
        query_embedding: np.ndarray,
        chunks: List[TextChunk],
        chunk_embeddings: List[np.ndarray],
    ) -> List[TextChunk]:
        """Select chunks using Maximum Marginal Relevance"""
        # Calculate similarities to query
        similarities = [np.dot(query_embedding, emb) for emb in chunk_embeddings]

        # Get top-k for reranking
        top_indices = np.argsort(similarities)[-self.config.rerank_top_k :]
        selected_indices = []

        # MMR selection
        while len(selected_indices) < self.config.top_k:
            best_score = -np.inf
            best_idx = -1

            for idx in top_indices:
                if idx in selected_indices:
                    continue

                # Calculate MMR score
                sim_query = similarities[idx]

                if not selected_indices:
                    mmr_score = sim_query
                else:
                    # Calculate similarity to already selected chunks
                    sim_selected = max(
                        np.dot(chunk_embeddings[idx], chunk_embeddings[sel_idx])
                        for sel_idx in selected_indices
                    )
                    mmr_score = (
                        self.config.mmr_lambda * sim_query
                        - (1 - self.config.mmr_lambda) * sim_selected
                    )

                if mmr_score > best_score:
                    best_score = mmr_score
                    best_idx = idx

            if best_idx == -1:
                break

            selected_indices.append(best_idx)

        return [chunks[idx] for idx in selected_indices]

    async def _similarity_selection(
        self,
        query_embedding: np.ndarray,
        chunks: List[TextChunk],
        chunk_embeddings: List[np.ndarray],
    ) -> List[TextChunk]:
        """Select chunks using simple similarity"""
        similarities = [np.dot(query_embedding, emb) for emb in chunk_embeddings]

        # Get top-k chunks
        top_indices = np.argsort(similarities)[-self.config.top_k :]
        return [chunks[idx] for idx in top_indices]
