"""Enhanced caching system with multiple backends"""

import asyncio
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from .base import BaseModule, ModuleConfig
from .exceptions import CacheError


class CacheBackend(ABC):
    """Abstract base class for cache backends"""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear all values from cache"""
        pass

    @abstractmethod
    async def has(self, key: str) -> bool:
        """Check if key exists in cache"""
        pass

    @abstractmethod
    async def touch(self, key: str, ttl: Optional[int] = None) -> bool:
        """Update key TTL"""
        pass


class MemoryBackend(CacheBackend):
    """In-memory cache implementation"""

    def __init__(self):
        self._cache: Dict[str, tuple[Any, Optional[datetime]]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None

        value, expiry = self._cache[key]
        if expiry and datetime.now() > expiry:
            await self.delete(key)
            return None

        return value

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        async with self._lock:
            expiry = datetime.now() + timedelta(seconds=ttl) if ttl else None
            self._cache[key] = (value, expiry)

    async def delete(self, key: str) -> None:
        async with self._lock:
            self._cache.pop(key, None)

    async def clear(self) -> None:
        async with self._lock:
            self._cache.clear()

    async def has(self, key: str) -> bool:
        if key not in self._cache:
            return False

        _, expiry = self._cache[key]
        if expiry and datetime.now() > expiry:
            await self.delete(key)
            return False

        return True

    async def touch(self, key: str, ttl: Optional[int] = None) -> bool:
        async with self._lock:
            if key not in self._cache:
                return False

            value, _ = self._cache[key]
            expiry = datetime.now() + timedelta(seconds=ttl) if ttl else None
            self._cache[key] = (value, expiry)
            return True


class CacheModule(BaseModule):
    """Advanced caching system with multiple backends"""

    __module_name__ = "cache"

    def __init__(self, config: Optional[ModuleConfig] = None):
        super().__init__(config or ModuleConfig())
        self._backend: Optional[CacheBackend] = None

    async def initialize(self) -> None:
        await super().initialize()
        self._backend = MemoryBackend()

    async def cleanup(self) -> None:
        if self._backend:
            await self._backend.clear()
        await super().cleanup()

    async def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache"""
        try:
            value = await self._backend.get(key)
            return value if value is not None else default
        except Exception as e:
            self._logger.error(f"Cache get error: {e}")
            return default

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        try:
            await self._backend.set(key, value, ttl)
        except Exception as e:
            self._logger.error(f"Cache set error: {e}")
            raise CacheError(f"Failed to set cache value: {e}") from e
