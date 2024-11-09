from dataclasses import dataclass
from typing import List, Optional, Tuple

import numpy as np
import torch
import torch.nn.functional as F
from sklearn.cluster import KMeans


@dataclass
class RoutingConfig:
    """Configuration for semantic routing"""

    num_clusters: int = 8
    min_cluster_size: int = 4
    similarity_threshold: float = 0.7
    use_dynamic_clusters: bool = True
    rerank_top_k: int = 10


class SemanticRouter:
    """Route queries to relevant document clusters"""

    def __init__(self, config: RoutingConfig):
        self.config = config
        self.clusters = None
        self.cluster_centers = None
        self.document_clusters = None

    def build_index(self, documents: List[str], embeddings: List[np.ndarray]) -> None:
        """Build routing index"""
        # Stack embeddings
        embedding_matrix = np.vstack(embeddings)

        # Determine optimal number of clusters if dynamic
        if self.config.use_dynamic_clusters:
            n_clusters = max(
                self.config.num_clusters, len(documents) // self.config.min_cluster_size
            )
        else:
            n_clusters = self.config.num_clusters

        # Cluster documents
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.clusters = kmeans.fit_predict(embedding_matrix)
        self.cluster_centers = kmeans.cluster_centers_

        # Store document-cluster mapping
        self.document_clusters = {
            i: [doc for doc, cluster in zip(documents, self.clusters) if cluster == i]
            for i in range(n_clusters)
        }

    async def route_query(
        self, query_embedding: np.ndarray, top_k: int = 3
    ) -> List[Tuple[int, float]]:
        """Find most relevant clusters for query"""
        # Calculate similarities to cluster centers
        similarities = [np.dot(query_embedding, center) for center in self.cluster_centers]

        # Get top-k clusters
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [
            (idx, similarities[idx])
            for idx in top_indices
            if similarities[idx] >= self.config.similarity_threshold
        ]

    def get_cluster_documents(self, cluster_id: int, limit: Optional[int] = None) -> List[str]:
        """Get documents from cluster"""
        docs = self.document_clusters.get(cluster_id, [])
        if limit:
            return docs[:limit]
        return docs

    def rerank_documents(
        self,
        query_embedding: np.ndarray,
        documents: List[str],
        document_embeddings: List[np.ndarray],
    ) -> List[Tuple[str, float]]:
        """Rerank documents using cross-attention"""
        if not documents:
            return []

        # Convert to tensors
        query_tensor = torch.from_numpy(query_embedding).unsqueeze(0)
        doc_tensor = torch.from_numpy(np.vstack(document_embeddings))

        # Calculate cross-attention scores
        attention = torch.matmul(query_tensor, doc_tensor.T)
        scores = F.softmax(attention, dim=-1).squeeze().numpy()

        # Sort documents by score
        ranked_docs = [(doc, score) for doc, score in zip(documents, scores)]
        ranked_docs.sort(key=lambda x: x[1], reverse=True)

        return ranked_docs[: self.config.rerank_top_k]
