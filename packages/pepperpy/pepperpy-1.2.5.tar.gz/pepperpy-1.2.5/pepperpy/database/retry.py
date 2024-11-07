import asyncio
from functools import wraps
from typing import Callable, Optional, Type, TypeVar, Union

from .exceptions import DatabaseError, TransactionError
from .types import RetryConfig

T = TypeVar("T")


class RetryHandler:
    """Handles database operation retries"""

    def __init__(self, config: RetryConfig) -> None:
        self.config = config

    async def retry(
        self,
        operation: Callable[..., T],
        *args: object,
        retry_on: Optional[Union[Type[Exception], tuple[Type[Exception], ...]]] = None,
        **kwargs: object,
    ) -> T:
        """Execute operation with retry logic"""
        if not self.config.enabled:
            return await operation(*args, **kwargs)

        retry_on = retry_on or (TransactionError, DatabaseError)
        attempt = 0
        last_error = None
        delay = self.config.delay

        while attempt < self.config.max_attempts:
            try:
                return await operation(*args, **kwargs)
            except retry_on as e:
                attempt += 1
                last_error = e

                if attempt == self.config.max_attempts:
                    break

                await asyncio.sleep(delay)
                delay *= self.config.backoff

        raise DatabaseError(
            f"Operation failed after {attempt} attempts: {str(last_error)}"
        ) from last_error


def with_retry(
    retry_on: Optional[Union[Type[Exception], tuple[Type[Exception], ...]]] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for adding retry logic to database operations"""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(self: object, *args: object, **kwargs: object) -> T:
            if not hasattr(self, "_retry_handler"):
                raise DatabaseError("RetryHandler not initialized")
            return await self._retry_handler.retry(func, self, *args, retry_on=retry_on, **kwargs)

        return wrapper

    return decorator
