from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import numpy as np
import spacy
from rank_bm25 import BM25Okapi
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class HybridSearchConfig:
    """Configuration for hybrid search"""

    semantic_weight: float = 0.7
    lexical_weight: float = 0.3
    top_k: int = 5
    min_score: float = 0.1
    use_reranking: bool = True
    reranking_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class HybridSearch:
    """Hybrid semantic and lexical search"""

    def __init__(self, config: HybridSearchConfig):
        self.config = config
        self.nlp = spacy.load("en_core_web_sm")

        # Initialize reranker if enabled
        if config.use_reranking:
            from sentence_transformers import CrossEncoder

            self.reranker = CrossEncoder(config.reranking_model)

    def preprocess_text(self, text: str) -> List[str]:
        """Preprocess text for lexical search"""
        doc = self.nlp(text)
        tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
        return tokens

    def build_index(
        self, texts: List[str], embeddings: List[np.ndarray]
    ) -> Tuple[BM25Okapi, np.ndarray]:
        """Build search indices"""
        # Preprocess texts for BM25
        tokenized_texts = [self.preprocess_text(text) for text in texts]
        bm25 = BM25Okapi(tokenized_texts)

        # Stack embeddings
        embedding_matrix = np.vstack(embeddings)

        return bm25, embedding_matrix

    async def search(
        self,
        query: str,
        query_embedding: np.ndarray,
        texts: List[str],
        bm25_index: BM25Okapi,
        embedding_matrix: np.ndarray,
    ) -> List[Dict[str, Any]]:
        """Perform hybrid search"""
        # Get lexical scores
        tokenized_query = self.preprocess_text(query)
        lexical_scores = np.array(bm25_index.get_scores(tokenized_query))

        # Get semantic scores
        semantic_scores = cosine_similarity(query_embedding.reshape(1, -1), embedding_matrix)[0]

        # Combine scores
        combined_scores = (
            self.config.semantic_weight * semantic_scores
            + self.config.lexical_weight * lexical_scores
        )

        # Get top results
        top_indices = np.argsort(combined_scores)[-self.config.top_k :][::-1]
        top_scores = combined_scores[top_indices]

        results = []
        for idx, score in zip(top_indices, top_scores):
            if score < self.config.min_score:
                continue

            result = {
                "text": texts[idx],
                "score": float(score),
                "semantic_score": float(semantic_scores[idx]),
                "lexical_score": float(lexical_scores[idx]),
            }
            results.append(result)

        # Rerank if enabled
        if self.config.use_reranking and results:
            pairs = [(query, result["text"]) for result in results]
            rerank_scores = self.reranker.predict(pairs)

            for result, rerank_score in zip(results, rerank_scores):
                result["rerank_score"] = float(rerank_score)

            results.sort(key=lambda x: x["rerank_score"], reverse=True)

        return results
