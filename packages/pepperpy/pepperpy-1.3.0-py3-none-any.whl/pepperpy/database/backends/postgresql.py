from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from ..types import ConnectionConfig, DatabaseConfig
from . import DatabaseBackend, register_backend


class PostgreSQLBackend(DatabaseBackend):
    """PostgreSQL database backend"""

    async def create_engine(
        self, connection: ConnectionConfig, **kwargs: Dict[str, Any]
    ) -> AsyncEngine:
        """Create PostgreSQL engine"""
        url = connection.url
        if not url.startswith("postgresql+asyncpg://"):
            url = f"postgresql+asyncpg://{url.removeprefix('postgresql://')}"

        return create_async_engine(url, **connection.options, **kwargs)

    async def run_migrations(self, engine: AsyncEngine, config: DatabaseConfig) -> None:
        """Run PostgreSQL migrations"""
        # Implement migration logic using alembic
        pass

    async def verify_connection(self, engine: AsyncEngine) -> bool:
        """Verify PostgreSQL connection"""
        try:
            async with engine.connect() as conn:
                await conn.execute("SELECT 1")
            return True
        except Exception:
            return False


# Register backend
register_backend("postgresql", PostgreSQLBackend)
