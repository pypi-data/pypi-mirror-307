import asyncio
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, AsyncIterator, Dict, List, Optional, Tuple

import numpy as np

from pepperpy.core import BaseModule
from pepperpy.core.exceptions import ModuleError

from .cache.memory import MemoryCache
from .embeddings.base import EmbeddingProvider, LocalEmbedding
from .metrics import AIMetric, MetricsCollector
from .processing import BatchProcessor
from .streaming import StreamingProvider, StreamingToken
from .templates import TemplateManager
from .text.chunking import ChunkingStrategy, SentenceChunker


class AIProvider(Enum):
    """Supported AI providers"""

    OPENROUTER = "openrouter"
    STACKSPOT = "stackspot"


@dataclass
class AIResponse:
    """Standardized AI response"""

    content: str
    model: str
    usage: Dict[str, int]
    metadata: Dict[str, Any]


class AIError(ModuleError):
    """Base exception for AI module errors"""

    pass


class ProviderNotFoundError(AIError):
    """Raised when provider is not found"""

    pass


class ModelNotFoundError(AIError):
    """Raised when model is not found"""

    pass


class BaseProvider(ABC):
    """Base class for AI providers"""

    @abstractmethod
    async def generate(self, prompt: str, model: Optional[str] = None, **kwargs) -> AIResponse:
        """Generate AI response"""
        pass

    @abstractmethod
    async def list_models(self) -> List[str]:
        """List available models"""
        pass


class AIModule(BaseModule):
    """Enhanced AI module with advanced capabilities"""

    __module_name__ = "ai"
    __version__ = "0.1.0"
    __description__ = "Multi-provider LLM integration module"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._providers: Dict[str, BaseProvider] = {}
        self._default_provider: Optional[str] = None
        self._chunker: ChunkingStrategy = SentenceChunker()
        self._embedding_provider: Optional[EmbeddingProvider] = None
        self._cache = MemoryCache()
        self._batch_processor = BatchProcessor(
            max_concurrent=config.get("max_concurrent", 3),
            max_batch_size=config.get("batch_size", 20),
        )
        self._template_manager = TemplateManager()
        self._metrics = MetricsCollector()

        # Load templates if configured
        if "templates_file" in self.config.settings:
            self._template_manager.load_from_file(self.config.settings["templates_file"])

    async def initialize(self) -> None:
        """Initialize AI providers and components"""
        await super().initialize()

        # Initialize embedding provider if configured
        if "embeddings" in self.config.settings:
            embedding_config = self.config.settings["embeddings"]
            if embedding_config.get("local", True):
                self._embedding_provider = LocalEmbedding(
                    model_name=embedding_config.get("model", "all-MiniLM-L6-v2")
                )

        # Initialize configured providers
        if "openrouter" in self.config.settings:
            from .providers.openrouter import OpenRouterProvider

            self._providers[AIProvider.OPENROUTER.value] = OpenRouterProvider(
                self.config.settings["openrouter"]
            )

        if "stackspot" in self.config.settings:
            from .providers.stackspot import StackSpotProvider

            self._providers[AIProvider.STACKSPOT.value] = StackSpotProvider(
                self.config.settings["stackspot"]
            )

        # Set default provider
        self._default_provider = self.config.settings.get("default_provider")
        if not self._default_provider and self._providers:
            self._default_provider = next(iter(self._providers))

    async def shutdown(self) -> None:
        """Cleanup AI providers"""
        self._providers.clear()
        await super().shutdown()

    async def generate(
        self,
        prompt: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs,
    ) -> AIResponse:
        """Generate AI response using specified or default provider"""
        provider_name = provider or self._default_provider
        if not provider_name:
            raise ProviderNotFoundError("No AI provider configured")

        provider_instance = self._providers.get(provider_name)
        if not provider_instance:
            raise ProviderNotFoundError(f"Provider not found: {provider_name}")

        try:
            return await provider_instance.generate(prompt, model, **kwargs)
        except Exception as e:
            self.logger.error(f"Generation failed: {str(e)}")
            raise AIError(f"Failed to generate response: {str(e)}") from e

    async def list_models(self, provider: Optional[str] = None) -> Dict[str, List[str]]:
        """List available models for specified or all providers"""
        if provider:
            provider_instance = self._providers.get(provider)
            if not provider_instance:
                raise ProviderNotFoundError(f"Provider not found: {provider}")
            return {provider: await provider_instance.list_models()}

        models = {}
        for name, provider_instance in self._providers.items():
            models[name] = await provider_instance.list_models()
        return models

    async def generate_with_context(
        self, prompt: str, context: str, max_chunk_size: int = 1000, **kwargs
    ) -> AIResponse:
        """Generate response with context support"""
        # Split context into chunks
        chunks = self._chunker.split(context, max_chunk_size)

        # If embedding provider exists, find most relevant chunks
        if self._embedding_provider:
            query_embedding = await self._embedding_provider.embed_text(prompt)
            chunk_embeddings = await self._embedding_provider.embed_batch(
                [chunk.content for chunk in chunks]
            )

            # Find most relevant chunks
            similarities = [np.dot(query_embedding, chunk_emb) for chunk_emb in chunk_embeddings]
            top_chunks = [chunks[i].content for i in np.argsort(similarities)[-3:]]  # Top 3 chunks

            # Build prompt with context
            context_prompt = "Context:\n" + "\n---\n".join(top_chunks) + "\n\nQuestion: " + prompt
        else:
            # Without embeddings, use simple concatenation
            context_prompt = f"Context:\n{context}\n\nQuestion: {prompt}"

        return await self.generate(context_prompt, **kwargs)

    async def embed_text(self, text: str) -> Optional[np.ndarray]:
        """Generate embeddings for text"""
        if not self._embedding_provider:
            self.logger.warning("No embedding provider configured")
            return None

        cache_key = f"emb:{text}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        embedding = await self._embedding_provider.embed_text(text)
        self._cache.set(cache_key, embedding)
        return embedding

    async def calculate_similarity(self, text1: str, text2: str) -> Optional[float]:
        """Calculate similarity between texts"""
        if not self._embedding_provider:
            self.logger.warning("No embedding provider configured")
            return None

        return await self._embedding_provider.similarity(text1, text2)

    async def generate_batch(
        self, prompts: List[str], batch_size: int = 5, **kwargs
    ) -> List[AIResponse]:
        """Generate multiple responses efficiently"""
        responses = []

        # Process in batches
        for i in range(0, len(prompts), batch_size):
            batch = prompts[i : i + batch_size]
            batch_responses = await asyncio.gather(
                *(self.generate(prompt, **kwargs) for prompt in batch)
            )
            responses.extend(batch_responses)

        return responses

    async def embed_batch(
        self, texts: List[str], batch_size: int = 20
    ) -> Optional[List[np.ndarray]]:
        """Generate embeddings for multiple texts efficiently"""
        if not self._embedding_provider:
            self.logger.warning("No embedding provider configured")
            return None

        embeddings = []
        cache_hits = 0

        # Process in batches
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            batch_embeddings = []

            # Check cache first
            for text in batch:
                cache_key = f"emb:{text}"
                cached = self._cache.get(cache_key)
                if cached is not None:
                    batch_embeddings.append(cached)
                    cache_hits += 1
                    continue

                # Add to list for batch processing
                batch_embeddings.append(text)

            # Process uncached texts
            if any(isinstance(x, str) for x in batch_embeddings):
                uncached_texts = [x for x in batch_embeddings if isinstance(x, str)]
                new_embeddings = await self._embedding_provider.embed_batch(uncached_texts)

                # Update cache
                for text, embedding in zip(uncached_texts, new_embeddings):
                    cache_key = f"emb:{text}"
                    self._cache.set(cache_key, embedding)

                # Replace strings with embeddings
                batch_embeddings = [
                    emb if isinstance(emb, np.ndarray) else new_embeddings.pop(0)
                    for emb in batch_embeddings
                ]

            embeddings.extend(batch_embeddings)

        self.logger.info(f"Embedding cache hits: {cache_hits}/{len(texts)}")
        return embeddings

    async def generate_stream(
        self, prompt: str, provider: Optional[str] = None, **kwargs
    ) -> AsyncIterator[StreamingToken]:
        """Generate streaming response"""
        provider_instance = self._get_provider(provider)
        if not isinstance(provider_instance, StreamingProvider):
            raise TypeError(f"Provider {provider} does not support streaming")

        async for token in provider_instance.stream(prompt, **kwargs):
            yield token

    async def process_document(
        self, document: str, queries: List[str], **kwargs
    ) -> Dict[str, AIResponse]:
        """Process document with multiple queries efficiently"""
        # Split document into optimal chunks
        chunks = self._chunker.split(document)

        # Generate embeddings for chunks in parallel
        chunk_embeddings = await self._batch_processor.process_batch(
            [chunk.content for chunk in chunks], self.embed_text
        )

        # Process queries in parallel
        async def process_query(query: str) -> Tuple[str, AIResponse]:
            # Find relevant chunks
            query_embedding = await self.embed_text(query)
            similarities = [np.dot(query_embedding, chunk_emb) for chunk_emb in chunk_embeddings]

            # Get top chunks
            top_indices = np.argsort(similarities)[-3:]
            context = "\n---\n".join(chunks[i].content for i in top_indices)

            # Generate response
            response = await self.generate_with_context(query, context, **kwargs)
            return query, response

        results = await self._batch_processor.process_batch(queries, process_query)

        return dict(results)

    async def analyze_similarities(self, texts: List[str], batch_size: int = 50) -> np.ndarray:
        """Compute similarity matrix for texts efficiently"""
        # Generate embeddings in batches
        embeddings = await self._batch_processor.process_batch(texts, self.embed_text)

        # Compute similarities in thread pool
        def compute_similarities(embs: List[np.ndarray]) -> np.ndarray:
            matrix = np.zeros((len(embs), len(embs)))
            for i in range(len(embs)):
                for j in range(i + 1, len(embs)):
                    sim = np.dot(embs[i], embs[j])
                    matrix[i, j] = sim
                    matrix[j, i] = sim
            return matrix

        return await self._batch_processor.run_in_thread(compute_similarities, embeddings)

    async def generate_from_template(
        self, template_name: str, variables: Dict[str, Any], **kwargs
    ) -> AIResponse:
        """Generate response using template"""
        start_time = time.time()
        success = False
        tokens = 0

        try:
            prompt = self._template_manager.render_template(template_name, **variables)
            if not prompt:
                raise ValueError(f"Template not found: {template_name}")

            response = await self.generate(prompt, **kwargs)
            success = True
            tokens = response.usage.get("total_tokens", 0)
            return response

        finally:
            duration = time.time() - start_time
            await self._metrics.add_metric(
                AIMetric(
                    operation="generate_template",
                    duration=duration,
                    tokens=tokens,
                    success=success,
                    metadata={"template": template_name, "variables": variables},
                )
            )

    def get_metrics(self) -> Dict[str, Any]:
        """Get module metrics"""
        return self._metrics.get_stats()

    def export_metrics(self, path: str) -> None:
        """Export metrics to file"""
        self._metrics.export_metrics(path)
