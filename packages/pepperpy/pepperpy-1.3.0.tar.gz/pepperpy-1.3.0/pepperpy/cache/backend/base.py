from abc import ABC, abstractmethod
from typing import Any, Optional


class CacheBackend(ABC):
    """Base class for cache backends"""

    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to cache backend"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection to cache backend"""
        pass

    @abstractmethod
    async def get(self, key: str) -> Any:
        """Retrieve value from cache"""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store value in cache"""
        pass
