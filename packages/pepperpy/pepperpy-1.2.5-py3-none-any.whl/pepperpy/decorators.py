import time
from functools import wraps
from typing import Any, Callable

from .console import Console

console = Console()


def timer(func: Callable) -> Callable:
    """Mede o tempo de execução"""

    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        console.info(f"{func.__name__} took {elapsed:.2f}s")
        return result

    return wrapper


def log_calls(func: Callable) -> Callable:
    """Loga chamadas de função"""

    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> Any:
        console.info(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


def retry(attempts: int = 3, delay: float = 1.0) -> Callable:
    """Tenta executar função múltiplas vezes"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Any:
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == attempts - 1:
                        raise
                    console.warning(f"Attempt {i+1} failed: {e}")
                    time.sleep(delay)

        return wrapper

    return decorator
