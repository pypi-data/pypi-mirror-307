"""Resource management and cleanup system"""

from contextlib import asynccontextmanager
from types import TracebackType
from typing import Any, AsyncIterator, Dict, Optional, Type

from .logging import get_logger

logger = get_logger("core.resources")


class ResourceManager:
    """Global resource manager for PepperPy modules"""

    def __init__(self):
        self._resources: Dict[str, Any] = {}
        self._logger = logger

    async def __aenter__(self) -> "ResourceManager":
        """Enter context"""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Exit context and cleanup resources"""
        await self.cleanup()

    async def add(self, name: str, resource: Any) -> None:
        """Add resource to manager"""
        self._resources[name] = resource
        self._logger.debug(f"Added resource: {name}")

    async def get(self, name: str) -> Any:
        """Get resource by name"""
        return self._resources.get(name)

    async def cleanup(self) -> None:
        """Cleanup all resources"""
        for name, resource in self._resources.items():
            try:
                if hasattr(resource, "cleanup"):
                    await resource.cleanup()
                self._logger.debug(f"Cleaned up resource: {name}")
            except Exception as e:
                self._logger.error(f"Error cleaning up {name}: {str(e)}")
        self._resources.clear()


# Singleton instance
manager = ResourceManager()


@asynccontextmanager
async def pepperpy_session() -> AsyncIterator[ResourceManager]:
    """Create a managed PepperPy session"""
    async with manager:
        yield manager
