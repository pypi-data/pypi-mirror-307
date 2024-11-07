from typing import Any, Dict

import duckdb
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from ..types import ConnectionConfig, DatabaseConfig
from . import DatabaseBackend, register_backend


class DuckDBBackend(DatabaseBackend):
    """DuckDB backend for analytics"""

    async def create_engine(
        self, connection: ConnectionConfig, **kwargs: Dict[str, Any]
    ) -> AsyncEngine:
        """Create DuckDB engine"""
        # DuckDB doesn't support async natively, so we wrap it
        url = f"duckdb:///{connection.url}"
        return create_async_engine(
            url,
            **connection.options,
            **kwargs,
            poolclass=None,  # DuckDB doesn't need connection pooling
        )

    async def run_migrations(self, engine: AsyncEngine, config: DatabaseConfig) -> None:
        """Run DuckDB migrations"""
        # DuckDB typically doesn't need migrations, but we can create tables
        async with engine.begin() as conn:
            await conn.run_sync(self._create_tables)

    def _create_tables(self, connection: duckdb.DuckDBPyConnection) -> None:
        """Create necessary tables"""
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """
        )

    async def verify_connection(self, engine: AsyncEngine) -> bool:
        """Verify DuckDB connection"""
        try:
            async with engine.connect() as conn:
                await conn.execute(duckdb.sql("SELECT 1"))
            return True
        except Exception:
            return False


# Register backend
register_backend("duckdb", DuckDBBackend)
