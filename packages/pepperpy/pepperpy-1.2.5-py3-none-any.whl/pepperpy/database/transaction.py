from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import DatabaseError

T = TypeVar("T")


class Transaction:
    """
    Transaction manager with support for nested transactions and savepoints
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._depth = 0

    @asynccontextmanager
    async def begin(self, **kwargs: Any) -> AsyncGenerator[AsyncSession, None]:
        """Begin a new transaction or savepoint"""
        self._depth += 1
        try:
            if self._depth == 1:
                async with self.session.begin(**kwargs):
                    yield self.session
            else:
                # Create savepoint for nested transaction
                async with self.session.begin_nested():
                    yield self.session
        except Exception as e:
            raise DatabaseError(f"Transaction failed: {e!s}") from e
        finally:
            self._depth -= 1

    async def commit(self) -> None:
        """Commit the current transaction"""
        if self._depth == 0:
            raise DatabaseError("No transaction in progress")
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback the current transaction"""
        if self._depth == 0:
            raise DatabaseError("No transaction in progress")
        await self.session.rollback()

    @property
    def in_transaction(self) -> bool:
        """Check if currently in a transaction"""
        return self._depth > 0
