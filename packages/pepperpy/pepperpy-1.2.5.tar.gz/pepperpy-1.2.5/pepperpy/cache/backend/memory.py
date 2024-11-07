from time import time
from typing import Any, Dict, Optional

from .base import CacheBackend


class MemoryCache(CacheBackend):
    """In-memory cache implementation"""

    def __init__(self) -> None:
        self._storage: Dict[str, tuple[Any, Optional[float]]] = {}

    async def connect(self) -> None:
        """No connection needed for memory cache"""
        pass

    async def disconnect(self) -> None:
        """Clear cache on disconnect"""
        self._storage.clear()

    async def get(self, key: str) -> Any:
        """Retrieve value from memory cache"""
        if key not in self._storage:
            return None

        value, expires_at = self._storage[key]
        if expires_at and time() > expires_at:
            del self._storage[key]
            return None

        return value

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store value in memory cache"""
        expires_at = time() + ttl if ttl else None
        self._storage[key] = (value, expires_at)
