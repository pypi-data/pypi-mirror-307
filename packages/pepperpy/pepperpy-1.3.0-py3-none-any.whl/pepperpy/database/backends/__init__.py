from abc import ABC, abstractmethod
from typing import Dict, Type

from sqlalchemy.ext.asyncio import AsyncEngine

from ..types import ConnectionConfig, DatabaseConfig


class DatabaseBackend(ABC):
    """Base class for database backends"""

    @abstractmethod
    async def create_engine(
        self,
        connection: ConnectionConfig,
        **kwargs: Dict[str, str | int | bool | float],
    ) -> AsyncEngine:
        """Create database engine"""
        pass

    @abstractmethod
    async def run_migrations(self, engine: AsyncEngine, config: DatabaseConfig) -> None:
        """Run database migrations"""
        pass

    @abstractmethod
    async def verify_connection(self, engine: AsyncEngine) -> bool:
        """Verify database connection"""
        pass


# Register available backends
_BACKENDS: Dict[str, Type[DatabaseBackend]] = {}


def register_backend(name: str, backend_class: Type[DatabaseBackend]) -> None:
    """Register database backend"""
    _BACKENDS[name] = backend_class


def get_backend(name: str) -> DatabaseBackend:
    """Get database backend by name"""
    if name not in _BACKENDS:
        raise ValueError(f"Unknown database backend: {name}")
    return _BACKENDS[name]()
