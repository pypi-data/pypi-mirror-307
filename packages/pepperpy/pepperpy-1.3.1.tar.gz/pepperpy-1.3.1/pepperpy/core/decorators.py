"""Core decorators for common patterns and functionality"""

import asyncio
import inspect
import logging
import time
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional, Type, TypeVar

from .exceptions import PepperPyError
from .metrics import Metric

T = TypeVar("T")


def timer(metric_name: Optional[str] = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Measure execution time and optionally record as metric

    Args:
        metric_name: Optional name for the metric to record
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            start = time.time()
            try:
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                return result
            finally:
                elapsed = time.time() - start
                if metric_name and hasattr(args[0], "metrics"):
                    metric = Metric(
                        name=metric_name,
                        value=elapsed,
                        timestamp=datetime.now(),
                        labels={"function": func.__name__},
                    )
                    await args[0].metrics.record(metric)
                logging.getLogger(func.__module__).debug(f"{func.__name__} took {elapsed:.3f}s")

        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> T:
            start = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                elapsed = time.time() - start
                logging.getLogger(func.__module__).debug(f"{func.__name__} took {elapsed:.3f}s")

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator


def retry(
    attempts: int = 3,
    delay: float = 1.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,),
    logger: Optional[logging.Logger] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Retry function on failure with exponential backoff

    Args:
        attempts: Maximum number of retry attempts
        delay: Initial delay between retries (doubles each attempt)
        exceptions: Tuple of exceptions to catch and retry
        logger: Optional logger instance
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            _logger = logger or logging.getLogger(func.__module__)
            current_delay = delay

            for attempt in range(attempts):
                try:
                    if asyncio.iscoroutinefunction(func):
                        return await func(*args, **kwargs)
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == attempts - 1:
                        raise
                    _logger.warning(f"Attempt {attempt + 1}/{attempts} failed: {str(e)}")
                    await asyncio.sleep(current_delay)
                    current_delay *= 2

            raise PepperPyError(f"All {attempts} retry attempts failed")

        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> T:
            _logger = logger or logging.getLogger(func.__module__)
            current_delay = delay

            for attempt in range(attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == attempts - 1:
                        raise
                    _logger.warning(f"Attempt {attempt + 1}/{attempts} failed: {str(e)}")
                    time.sleep(current_delay)
                    current_delay *= 2

            raise PepperPyError(f"All {attempts} retry attempts failed")

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator


def validate_args(
    **validators: Callable[[Any], bool],
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Validate function arguments using provided validator functions

    Args:
        validators: Dict mapping argument names to validator functions
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            # Combine args and kwargs
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Validate arguments
            for arg_name, validator in validators.items():
                if arg_name in bound_args.arguments:
                    value = bound_args.arguments[arg_name]
                    if not validator(value):
                        raise ValueError(f"Validation failed for argument {arg_name}")

            return func(*args, **kwargs)

        return wrapper

    return decorator
