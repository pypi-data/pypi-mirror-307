import time
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Optional, Type, TypeVar, Union

if TYPE_CHECKING:
    from .module import DatabaseClass

from .constants import DatabaseEvents
from .events import QueryExecuted
from .exceptions import DatabaseError, TransactionError

T = TypeVar("T")


def transactional(auto_commit: bool = True) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for transactional operations"""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(
            self: "DatabaseClass", *args: tuple[Any, ...], **kwargs: dict[str, Any]
        ) -> T:
            async with self.transaction.begin() as session:
                result = await func(self, session, *args, **kwargs)
                if auto_commit:
                    await session.commit()
                return result

        return wrapper

    return decorator


def measure_query(name: Optional[str] = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for measuring query execution time"""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(
            self: "DatabaseClass", *args: tuple[Any, ...], **kwargs: dict[str, Any]
        ) -> T:
            query_name = name or func.__name__
            start_time = time.time()
            try:
                result = await func(self, *args, **kwargs)
                duration = time.time() - start_time

                # Emit metrics event
                await self.emit(
                    DatabaseEvents.QUERY_EXECUTED,
                    QueryExecuted(query=query_name, duration=duration),
                )
                return result
            except Exception as e:
                duration = time.time() - start_time
                # Log error metrics
                self._metrics.record_error(e)
                raise

        return wrapper

    return decorator


def retry_on_error(
    exceptions: Optional[Union[Type[Exception], tuple[Type[Exception], ...]]] = None,
    max_attempts: int = 3,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for retrying operations on specific errors"""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(
            self: "DatabaseClass", *args: tuple[Any, ...], **kwargs: dict[str, Any]
        ) -> T:
            if not hasattr(self, "_retry_handler"):
                raise DatabaseError("RetryHandler not initialized")

            return await self._retry_handler.retry(
                func,
                self,
                *args,
                retry_on=exceptions or (DatabaseError, TransactionError),
                max_attempts=max_attempts,
                **kwargs,
            )

        return wrapper

    return decorator
