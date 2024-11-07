from typing import Optional

from ..core import BaseModule
from .backend.base import CacheBackend
from .backend.memory import MemoryCache


class CacheModule(BaseModule):
    """Cache management module"""

    __module_name__ = "cache"

    def __init__(self, config: Optional[dict] = None) -> None:
        super().__init__(config)
        self._backend: Optional[CacheBackend] = None

    async def setup(self) -> None:
        """Initialize cache backend"""
        backend_type = self.config.get("backend", "memory")
        if backend_type == "memory":
            self._backend = MemoryCache()
        else:
            raise ValueError(f"Unsupported cache backend: {backend_type}")

        await self._backend.connect()
        await super().setup()
