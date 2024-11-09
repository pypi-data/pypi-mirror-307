import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import AsyncIterator, Optional


@dataclass
class StreamingToken:
    """Represents a streaming token"""

    content: str
    index: int
    metadata: Optional[dict] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class StreamingStats:
    """Statistics for streaming response"""

    total_tokens: int = 0
    tokens_per_second: float = 0
    duration: float = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class StreamingProvider(ABC):
    """Base class for streaming providers"""

    @abstractmethod
    async def stream(
        self, prompt: str, buffer_size: int = 5, **kwargs
    ) -> AsyncIterator[StreamingToken]:
        """Stream response tokens with buffering"""
        pass


class StreamingResponse:
    """Enhanced streaming response manager"""

    def __init__(self, buffer_size: int = 5):
        self._buffer = []
        self._index = 0
        self._buffer_size = buffer_size
        self._queue = asyncio.Queue(maxsize=buffer_size)
        self._stats = StreamingStats()

    async def add_token(self, content: str, metadata: Optional[dict] = None) -> StreamingToken:
        """Add token to response with backpressure"""
        token = StreamingToken(content, self._index, metadata)

        # Initialize stats if first token
        if self._index == 0:
            self._stats.start_time = datetime.utcnow()

        # Add to buffer
        self._buffer.append(token)
        self._index += 1

        # Update stats
        self._stats.total_tokens = self._index
        if self._stats.start_time:
            duration = (datetime.utcnow() - self._stats.start_time).total_seconds()
            self._stats.tokens_per_second = self._index / duration
            self._stats.duration = duration

        # Wait if buffer is full
        await self._queue.put(token)
        return token

    async def get_tokens(self) -> AsyncIterator[StreamingToken]:
        """Get tokens as they become available"""
        try:
            while True:
                token = await self._queue.get()
                yield token
                self._queue.task_done()
        except asyncio.CancelledError:
            self._stats.end_time = datetime.utcnow()

    @property
    def content(self) -> str:
        """Get complete response content"""
        return "".join(token.content for token in self._buffer)

    @property
    def stats(self) -> StreamingStats:
        """Get streaming statistics"""
        return self._stats
