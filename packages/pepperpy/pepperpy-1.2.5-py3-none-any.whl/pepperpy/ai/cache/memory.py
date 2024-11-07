import time
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class CacheEntry:
    """Cache entry with TTL"""

    value: Any
    expires_at: Optional[float]


class MemoryCache:
    """In-memory cache for AI responses and embeddings"""

    def __init__(self, default_ttl: Optional[int] = 3600):
        self._cache: Dict[str, CacheEntry] = {}
        self._default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        entry = self._cache.get(key)
        if not entry:
            return None

        if entry.expires_at and time.time() > entry.expires_at:
            del self._cache[key]
            return None

        return entry.value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        expires_at = None
        if ttl or self._default_ttl:
            expires_at = time.time() + (ttl or self._default_ttl)

        self._cache[key] = CacheEntry(value, expires_at)

    def clear(self) -> None:
        """Clear cache"""
        self._cache.clear()
