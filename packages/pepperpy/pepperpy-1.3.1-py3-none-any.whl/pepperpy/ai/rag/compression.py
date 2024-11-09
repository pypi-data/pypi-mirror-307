from dataclasses import dataclass
from typing import List, Optional

import numpy as np
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


@dataclass
class CompressionConfig:
    """Configuration for context compression"""

    max_length: int = 512
    stride: int = 128
    compression_ratio: float = 0.5
    model_name: str = "facebook/bart-large-cnn"
    min_relevance: float = 0.3
    use_clustering: bool = True
    num_clusters: int = 3


class ContextCompressor:
    """Compress and optimize context for RAG"""

    def __init__(self, config: CompressionConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            config.model_name, num_labels=1
        )

        if torch.cuda.is_available():
            self.model = self.model.cuda()

    def compress_chunks(
        self, chunks: List[str], query: str, scores: Optional[List[float]] = None
    ) -> List[str]:
        """Compress and optimize context chunks"""
        # Score chunks if not provided
        if scores is None:
            scores = self._score_relevance(chunks, query)

        # Filter by relevance
        relevant_chunks = [
            chunk for chunk, score in zip(chunks, scores) if score >= self.config.min_relevance
        ]

        if not relevant_chunks:
            return chunks[:1]  # Return at least one chunk

        # Cluster similar chunks if enabled
        if self.config.use_clustering:
            compressed_chunks = self._cluster_chunks(relevant_chunks)
        else:
            # Take top chunks based on compression ratio
            num_chunks = max(1, int(len(relevant_chunks) * self.config.compression_ratio))
            compressed_chunks = relevant_chunks[:num_chunks]

        return compressed_chunks

    def _score_relevance(self, chunks: List[str], query: str) -> List[float]:
        """Score chunk relevance to query"""
        pairs = [(query, chunk) for chunk in chunks]

        # Tokenize
        inputs = self.tokenizer(
            pairs,
            padding=True,
            truncation=True,
            max_length=self.config.max_length,
            return_tensors="pt",
        )

        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}

        # Get relevance scores
        with torch.no_grad():
            outputs = self.model(**inputs)
            scores = torch.sigmoid(outputs.logits).cpu().numpy().flatten()

        return scores.tolist()

    def _cluster_chunks(self, chunks: List[str]) -> List[str]:
        """Cluster similar chunks"""
        from sentence_transformers import SentenceTransformer
        from sklearn.cluster import KMeans

        # Get embeddings
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(chunks)

        # Cluster
        n_clusters = min(self.config.num_clusters, len(chunks))
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(embeddings)

        # Select representative chunks
        compressed = []
        for i in range(n_clusters):
            cluster_chunks = [chunk for chunk, cluster in zip(chunks, clusters) if cluster == i]
            if cluster_chunks:
                # Take chunk closest to cluster center
                cluster_center = kmeans.cluster_centers_[i]
                chunk_embeddings = model.encode(cluster_chunks)
                distances = np.linalg.norm(chunk_embeddings - cluster_center, axis=1)
                best_idx = np.argmin(distances)
                compressed.append(cluster_chunks[best_idx])

        return compressed
