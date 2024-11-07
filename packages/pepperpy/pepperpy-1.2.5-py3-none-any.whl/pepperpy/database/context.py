from contextlib import asynccontextmanager
from typing import Any, Optional, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from pepperpy.core.context import Context

from .exceptions import DatabaseError
from .models import BaseModel

T = TypeVar("T", bound=BaseModel)


class DatabaseContext:
    """Database context manager for session and transaction handling"""

    def __init__(self, context: Context):
        self._context = context
        self._session: Optional[AsyncSession] = None

    @property
    def session(self) -> AsyncSession:
        """Get current session"""
        if not self._session:
            raise DatabaseError("No active database session")
        return self._session

    @asynccontextmanager
    async def transaction(self) -> AsyncSession:
        """Transaction context manager"""
        if not self._session:
            raise DatabaseError("No active database session")
        async with self._session.begin():
            yield self._session

    def set_session(self, session: AsyncSession) -> None:
        """Set current session"""
        self._session = session

    def clear_session(self) -> None:
        """Clear current session"""
        self._session = None

    def get_state(self, key: str, default: Any = None) -> Any:
        """Get state from context"""
        return self._context.get_state(f"database.{key}", default)

    def set_state(self, key: str, value: Any) -> None:
        """Set state in context"""
        self._context.set_state(f"database.{key}", value)
