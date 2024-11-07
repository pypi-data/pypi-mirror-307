import hashlib
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

import numpy as np


class CacheBackend(ABC):
    """Base class for cache backends"""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear cache"""
        pass

    def make_key(self, *args, **kwargs) -> str:
        """Create consistent cache key"""
        # Create deterministic string from args and kwargs
        key_parts = [str(arg) for arg in args]
        key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
        key_str = ":".join(key_parts)

        # Create hash for long keys
        if len(key_str) > 250:  # Keep keys manageable
            return hashlib.sha256(key_str.encode()).hexdigest()
        return key_str


class FileCache(CacheBackend):
    """Simple file-based cache for embeddings"""

    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    async def get(self, key: str) -> Optional[Any]:
        file_path = self.cache_dir / f"{key}.json"
        if not file_path.exists():
            return None

        try:
            data = json.loads(file_path.read_text())
            if data.get("type") == "numpy":
                return np.array(data["value"])
            return data["value"]
        except Exception:
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        file_path = self.cache_dir / f"{key}.json"

        if isinstance(value, np.ndarray):
            data = {"type": "numpy", "value": value.tolist()}
        else:
            data = {"type": "raw", "value": value}

        file_path.write_text(json.dumps(data))

    async def clear(self) -> None:
        for file in self.cache_dir.glob("*.json"):
            file.unlink()
