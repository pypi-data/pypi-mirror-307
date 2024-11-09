import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncGenerator, Dict, List, Optional, TypeVar, Union

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from pepperpy.core import BaseModule, ModuleConfig
from pepperpy.core.exceptions import DatabaseError
from pepperpy.core.types import JsonDict

from .migrations import MigrationManager

T = TypeVar("T")


@dataclass
class DatabaseConfig(ModuleConfig):
    """Database configuration"""

    url: str
    pool_size: int = 5
    max_overflow: int = 10
    echo: bool = False
    pool_timeout: float = 30.0
    pool_recycle: int = 3600
    ssl: bool = False
    retry_attempts: int = 3
    retry_delay: float = 1.0
    migrate: bool = True
    isolation_level: str = "READ COMMITTED"
    statement_timeout: int = 30000  # milliseconds
    timezone: str = "UTC"


class DatabaseModule(BaseModule):
    """Enhanced database management with migrations and query building"""

    __module_name__ = "database"
    __dependencies__ = ["cache", "metrics"]

    def __init__(self, config: Optional[DatabaseConfig] = None):
        super().__init__(config or DatabaseConfig())
        self._engine = None
        self._session_factory = None
        self._migration_manager = None
        self._lock = asyncio.Lock()
        self._active_sessions: Dict[int, AsyncSession] = {}

    async def initialize(self) -> None:
        """Initialize database connection and migrations"""
        await super().initialize()

        try:
            self._engine = create_async_engine(
                self.config.url,
                echo=self.config.echo,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_recycle=self.config.pool_recycle,
                pool_timeout=self.config.pool_timeout,
                connect_args={
                    "statement_timeout": self.config.statement_timeout,
                    "timezone": self.config.timezone,
                    "ssl": self.config.ssl,
                },
            )

            self._session_factory = sessionmaker(
                self._engine, class_=AsyncSession, expire_on_commit=False
            )

            if self.config.migrate:
                self._migration_manager = MigrationManager(self._engine)
                await self._migration_manager.run_migrations()

        except Exception as e:
            raise DatabaseError(f"Failed to initialize database: {e}") from e

    async def cleanup(self) -> None:
        """Cleanup database connections"""
        if self._engine:
            # Close all active sessions
            for session in self._active_sessions.values():
                await session.close()
            self._active_sessions.clear()

            # Dispose engine
            await self._engine.dispose()

        await super().cleanup()

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session with automatic cleanup

        Yields:
            AsyncSession: Database session that will be automatically cleaned up
        """
        session = self._session_factory()
        session_id = id(session)

        try:
            self._active_sessions[session_id] = session
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise DatabaseError(f"Database session error: {e}") from e
        finally:
            await session.close()
            del self._active_sessions[session_id]

    async def execute(
        self, query: Union[str, text], params: Optional[Dict[str, Any]] = None, **kwargs
    ) -> Any:
        """Execute raw SQL query with retry support"""
        attempts = self.config.retry_attempts
        delay = self.config.retry_delay

        while attempts > 0:
            try:
                async with self.session() as session:
                    result = await session.execute(
                        text(query) if isinstance(query, str) else query, params or {}, **kwargs
                    )
                    return result
            except Exception as e:
                attempts -= 1
                if attempts == 0:
                    raise DatabaseError(f"Query execution failed: {e}") from e
                await asyncio.sleep(delay)
                delay *= 2

    async def fetch_one(
        self, query: Union[str, text], params: Optional[Dict[str, Any]] = None, **kwargs
    ) -> Optional[JsonDict]:
        """Fetch single result as dictionary"""
        result = await self.execute(query, params, **kwargs)
        row = result.first()
        return dict(row._mapping) if row else None

    async def fetch_all(
        self, query: Union[str, text], params: Optional[Dict[str, Any]] = None, **kwargs
    ) -> List[JsonDict]:
        """Fetch multiple results as dictionaries"""
        result = await self.execute(query, params, **kwargs)
        return [dict(row._mapping) for row in result.all()]

    async def fetch_value(
        self, query: Union[str, text], params: Optional[Dict[str, Any]] = None, **kwargs
    ) -> Any:
        """Fetch single value"""
        result = await self.execute(query, params, **kwargs)
        return result.scalar()
