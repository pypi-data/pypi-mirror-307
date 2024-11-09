"""Context management and dependency injection"""

import logging
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Dict, Generator, Optional, Type, TypeVar

T = TypeVar("T")


@dataclass
class ContextVar:
    """Context variable definition"""

    name: str
    value: Any
    scope: str = "request"  # request, session, or application


class Context:
    """Request context management"""

    _current: Dict[str, Any] = {}

    @classmethod
    def get_current(cls) -> Optional["Context"]:
        """Get current context"""
        return getattr(cls._current, "current", None)

    @classmethod
    @contextmanager
    def enter_scope(cls, **kwargs) -> Generator[None, None, None]:
        """Enter new context scope

        Args:
            **kwargs: Context variables to set

        Yields:
            None: Context scope
        """
        previous = cls.get_current()
        try:
            cls._current.update(kwargs)
            yield
        finally:
            cls._current = previous

    def __init__(self):
        self._values: Dict[str, ContextVar] = {}
        self._logger = logging.getLogger("pepperpy.context")

    def get(self, name: str, default: Optional[T] = None) -> Optional[T]:
        """Get context variable"""
        var = self._values.get(name)
        return var.value if var else default

    def set(self, name: str, value: Any, scope: str = "request") -> None:
        """Set context variable"""
        self._values[name] = ContextVar(name, value, scope)

    def remove(self, name: str) -> None:
        """Remove context variable"""
        self._values.pop(name, None)

    def clear(self, scope: Optional[str] = None) -> None:
        """Clear context variables"""
        if scope:
            self._values = {k: v for k, v in self._values.items() if v.scope != scope}
        else:
            self._values.clear()


class Inject:
    """Dependency injection decorator"""

    def __init__(self, **dependencies: Type):
        self.dependencies = dependencies

    def __call__(self, func):
        """Decorator to inject context variables"""

        def wrapper(*args, **kwargs):
            context = self.get_current()
            return func(*args, **kwargs, **context)

        return wrapper
