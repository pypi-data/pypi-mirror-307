from typing import Any, Dict, List, Optional, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from pepperpy.core import BaseModule
from pepperpy.core.types import Result

from .backends import DatabaseBackend, get_backend
from .cache import QueryCache
from .config import DatabaseConfigProvider
from .constants import DatabaseEvents
from .context import DatabaseContext
from .decorators import measure_query, retry_on_error, transactional
from .events import DatabaseEvent, ModelCreated, QueryExecuted
from .exceptions import ConnectionError, DatabaseError
from .hooks import HookManager
from .logging import DatabaseLogger
from .metrics import DatabaseMetrics
from .models import BaseModel
from .profiling import DatabaseProfiler
from .query import QueryBuilder
from .results import BatchResult, QueryResult
from .retry import RetryHandler
from .sql import SQLQueries
from .transaction import Transaction
from .types import DatabaseConfig
from .validation import database_validator

T = TypeVar("T", bound=BaseModel)
ModelType = TypeVar("ModelType", bound=BaseModel)


class DatabaseModule(BaseModule):
    """Database management module with comprehensive backend support.

    This module provides a unified interface for database operations across different
    backends, with built-in support for:
    - Connection pooling and management
    - Transaction handling
    - Query execution and result processing
    - Performance monitoring and profiling

    Args:
        config (Optional[Dict[str, Any]]): Module configuration including:
            - backend: Database backend type
            - connection_url: Database connection URL
            - pool_size: Connection pool size
            - debug: Enable debug mode

    Examples:
        >>> module = DatabaseModule({
        ...     "backend": "postgresql",
        ...     "connection_url": "postgresql://localhost/db"
        ... })
        >>> await module.setup()
        >>> async with module.transaction() as session:
        ...     result = await session.execute("SELECT * FROM users")
    """

    __module_name__ = "database"
    __version__ = "1.0.0"
    __description__ = "Database management with multiple backend support"
    __dependencies__ = []

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        # Use DatabaseConfigProvider
        config_provider = DatabaseConfigProvider(config or {})
        super().__init__(config_provider)

        self._engine: Optional[AsyncEngine] = None
        self._backend: Optional[DatabaseBackend] = None
        self._transaction_manager: Optional[Transaction] = None
        self._retry_handler: Optional[RetryHandler] = None
        self._logger = DatabaseLogger()
        self._metrics = DatabaseMetrics()
        self._validator = database_validator

        # Initialize base model class
        class Base(DeclarativeBase):
            pass

        self.Model = Base

        # Novos componentes
        self._context = DatabaseContext(self.context)
        self._cache = QueryCache()
        self._hooks = HookManager()

        # Adiciona profiler
        self._profiler = DatabaseProfiler(
            slow_threshold=self.config.settings.get("slow_query_threshold", 1.0)
        )

    async def pre_initialize(self) -> None:
        """Pre-initialization hook"""
        # Validate configuration
        if not self.config.settings.get("connection"):
            raise ConnectionError("Database connection configuration required")

        errors = self._validator.validate(self.config.settings)
        if errors:
            raise ConnectionError(f"Invalid configuration: {', '.join(errors)}")

    async def _initialize(self) -> None:
        """Initialize database connection"""
        try:
            # Load configuration
            db_config = DatabaseConfig(**self.config.settings)

            # Initialize components
            self._retry_handler = RetryHandler(db_config.retry)
            self._backend = get_backend(db_config.backend)
            self._engine = await self._backend.create_engine(db_config)
            self._transaction_manager = Transaction(self._engine)

            # Run migrations if enabled
            if db_config.auto_migrate:
                await self.emit(DatabaseEvents.MIGRATION_START, {})
                try:
                    await self._backend.run_migrations(self._engine, db_config)
                    await self.emit(DatabaseEvents.MIGRATION_COMPLETE, {})
                except Exception as e:
                    await self.emit(DatabaseEvents.MIGRATION_ERROR, {"error": str(e)})
                    raise

            # Update metrics
            self._metrics.update_pool_stats(db_config.pool.size, db_config.pool.size)

            # Initialize cache if enabled
            if self.config.settings.get("cache_enabled", True):
                self._cache = QueryCache(ttl=self.config.settings.get("cache_ttl", 300))

            # Emit ready event
            await self.emit(
                DatabaseEvents.READY, DatabaseEvent(data={"backend": db_config.backend})
            )

        except Exception as e:
            self._metrics.record_error(e)
            await self.emit(DatabaseEvents.ERROR, {"error": str(e)})
            raise DatabaseError(f"Database initialization failed: {e!s}") from e

    @measure_query()
    @retry_on_error()
    async def execute(
        self,
        query: str,
        params: Optional[Dict] = None,
        session: Optional[AsyncSession] = None,
    ) -> QueryResult[Any]:
        """Execute raw SQL query with retry and metrics"""
        # Start profiling
        query_profile = self._profiler.start_query(query, params)

        # Check cache first
        cache_key = f"{query}:{params!s}"
        if cached := self._cache.get(cache_key):
            self._profiler.record_cache_hit(query)
            return QueryResult(
                success=True,
                data=cached,
                query=query,
                params=params,
                execution_time=0.0,
            )

        try:
            async with self.transaction.session() as session:
                result = await session.execute(query, params or {})

                # Update profile
                self._profiler.end_query(query_profile, rows_affected=result.rowcount)

                query_result = QueryResult(
                    success=True,
                    data=result.fetchall(),
                    query=query,
                    params=params,
                    execution_time=query_profile.duration,
                    rows_affected=result.rowcount,
                )

                if query_result.success:
                    self._cache.set(cache_key, query_result.data)

                return query_result

        except Exception as e:
            # Update profile with error
            self._profiler.end_query(query_profile)
            return QueryResult(
                success=False,
                error_message=str(e),
                query=query,
                params=params,
                execution_time=query_profile.duration,
            )

    async def get_profile(self) -> Dict[str, Any]:
        """Get database profiling information"""
        profile = self._profiler.get_profile()

        # Update connection stats
        if self._engine:
            pool = self._engine.pool
            self._profiler.update_connection_stats(
                total=pool.size, active=pool.checkedin, idle=pool.checkedout
            )

        return profile.get_statistics()

    async def reset_profile(self) -> None:
        """Reset profiling data"""
        self._profiler.reset()

    async def batch_execute(self, queries: List[Dict[str, Any]]) -> BatchResult[Any]:
        """Execute multiple queries in a transaction"""
        total = len(queries)
        succeeded = 0
        failed = 0
        errors = []
        query_results = []  # Lista para armazenar resultados

        async with self.transaction.begin() as session:
            for query_data in queries:
                try:
                    result = await self.execute(
                        query_data["query"], query_data.get("params"), session=session
                    )
                    if result.success:
                        succeeded += 1
                        query_results.append(result)
                    else:
                        failed += 1
                        errors.append({"query": query_data, "error": result.error_message})
                except Exception as e:
                    failed += 1
                    errors.append({"query": query_data, "error": str(e)})

        return BatchResult(
            success=failed == 0,
            data=[r for r in query_results if r.success],
            total=total,
            succeeded=succeeded,
            failed=failed,
            errors=errors,
        )

    @transactional()
    async def bulk_insert(
        self, session: AsyncSession, table: str, records: List[Dict[str, Any]]
    ) -> Result[int]:
        """Bulk insert records with transaction"""
        try:
            result = await session.execute(
                f"INSERT INTO {table} ({','.join(records[0].keys())}) "
                f"VALUES ({','.join([':' + k for k in records[0].keys()])})",
                records,
            )
            return Result.ok(result.rowcount)
        except Exception as e:
            return Result.fail(str(e))

    async def get_table_info(self, table: str) -> Result[Dict[str, Any]]:
        """Get table information"""
        try:
            async with self.transaction.session() as session:
                # Get column information
                columns = await session.execute(
                    SQLQueries.GET_COLUMNS, {"table": table, "schema": "public"}
                )

                # Get table statistics
                size = await session.execute(SQLQueries.TABLE_SIZE, {"table": table})

                count = await session.execute(SQLQueries.ROW_COUNT, {"table": table})

                return Result.ok(
                    {
                        "columns": columns.fetchall(),
                        "size": size.scalar(),
                        "row_count": count.scalar(),
                    }
                )
        except Exception as e:
            return Result.fail(str(e))

    async def health_check(self) -> Result[bool]:
        """Check database health"""
        try:
            async with self.transaction.session() as session:
                await session.execute("SELECT 1")
            return Result.ok(True)
        except Exception as e:
            return Result.fail(str(e))

    # Event handlers
    async def _handle_model_created(self, event: ModelCreated) -> None:
        """Handle model created event"""
        self.logger.info(f"Model created: {event.model}")

    async def _handle_query_executed(self, event: QueryExecuted) -> None:
        """Handle query executed event"""
        self.logger.debug(f"Query executed: {event.query} (duration: {event.duration:.2f}s)")

    # Public API
    @property
    def transaction(self) -> Transaction:
        """Get transaction manager"""
        if not self._transaction_manager:
            raise DatabaseError("Transaction manager not initialized")
        return self._transaction_manager

    def query(self, model: Type[T]) -> QueryBuilder[T]:
        """Create query builder for model"""
        return QueryBuilder(model)

    async def create(self, model: Type[ModelType], **data: Dict[str, object]) -> Result[ModelType]:
        """Create model instance with hooks"""
        try:
            instance = model(**data)

            # Execute before hooks
            await self._hooks.execute_hooks("before_create", model, instance)

            async with self.transaction.session() as session:
                session.add(instance)
                await session.flush()

                # Execute after hooks
                await self._hooks.execute_hooks("after_create", model, instance)

                return Result.ok(instance)

        except Exception as e:
            return Result.fail(str(e))
