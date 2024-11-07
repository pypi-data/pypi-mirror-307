import time
from dataclasses import dataclass
from typing import Dict, Generic, Optional, TypeVar

T = TypeVar("T")


@dataclass
class CacheEntry(Generic[T]):
    """Cache entry with expiration"""

    value: T
    expires_at: float


class QueryCache(Generic[T]):
    """Simple query result cache"""

    def __init__(self, ttl: int = 300) -> None:  # 5 minutes default TTL
        self._cache: Dict[str, CacheEntry[T]] = {}
        self._ttl = ttl

    def get(self, key: str) -> Optional[T]:
        """Get cached value if not expired"""
        if key not in self._cache:
            return None

        entry = self._cache[key]
        if time.time() > entry.expires_at:
            del self._cache[key]
            return None

        return entry.value

    def set(self, key: str, value: T, ttl: Optional[int] = None) -> None:
        """Set cache value with expiration"""
        expires_at = time.time() + (ttl or self._ttl)
        self._cache[key] = CacheEntry(value, expires_at)

    def invalidate(self, key: str) -> None:
        """Remove key from cache"""
        self._cache.pop(key, None)

    def clear(self) -> None:
        """Clear all cached values"""
        self._cache.clear()
