from typing import Any, Dict, List

import numpy as np

from ..module import AIModule
from .base import Pipeline


class AIPipelines:
    """Common AI pipeline templates"""

    @staticmethod
    def create_rag_pipeline(ai_module: "AIModule", chunk_size: int = 1000) -> Pipeline:
        """Create RAG (Retrieval Augmented Generation) pipeline"""
        pipeline = Pipeline("rag")

        # Add chunking step
        async def chunk_text(text: str, **kwargs) -> List[str]:
            chunks = ai_module._chunker.split(text, chunk_size)
            return [chunk.content for chunk in chunks]

        pipeline.add_step("chunk", chunk_text)

        # Add embedding step
        async def generate_embeddings(chunks: List[str], **kwargs) -> List[np.ndarray]:
            return await ai_module.embed_batch(chunks)

        pipeline.add_step("embed", generate_embeddings)

        # Add similarity search step
        async def find_relevant(
            data: Dict[str, Any], query: str, top_k: int = 3, **kwargs
        ) -> List[str]:
            query_embedding = await ai_module.embed_text(query)
            chunks, embeddings = data["chunks"], data["embeddings"]

            # Calculate similarities
            similarities = [np.dot(query_embedding, emb) for emb in embeddings]

            # Get top chunks
            top_indices = np.argsort(similarities)[-top_k:]
            return [chunks[i] for i in top_indices]

        pipeline.add_step("search", find_relevant)

        # Add generation step
        async def generate_response(context: List[str], query: str, **kwargs) -> str:
            context_text = "\n---\n".join(context)
            response = await ai_module.generate_with_context(query, context_text, **kwargs)
            return response.content

        pipeline.add_step("generate", generate_response)

        return pipeline

    @staticmethod
    def create_batch_processing_pipeline(ai_module: "AIModule", batch_size: int = 5) -> Pipeline:
        """Create batch processing pipeline"""
        pipeline = Pipeline("batch_processing")

        # Add batching step
        async def create_batches(items: List[Any], **kwargs) -> List[List[Any]]:
            return [items[i : i + batch_size] for i in range(0, len(items), batch_size)]

        pipeline.add_step("batch", create_batches)

        # Add processing step
        async def process_batch(batch: List[Any], **kwargs) -> List[Any]:
            return await ai_module.generate_batch(batch, **kwargs)

        pipeline.add_step("process", process_batch)

        # Add result collection step
        async def collect_results(batches: List[List[Any]], **kwargs) -> List[Any]:
            results = []
            for batch in batches:
                results.extend(batch)
            return results

        pipeline.add_step("collect", collect_results)

        return pipeline
