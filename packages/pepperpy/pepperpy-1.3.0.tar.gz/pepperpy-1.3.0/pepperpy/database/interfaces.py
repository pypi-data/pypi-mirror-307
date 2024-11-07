from abc import ABC, abstractmethod
from typing import Dict, Generic, Optional, TypeVar, Union

from sqlalchemy.ext.asyncio import AsyncSession

from pepperpy.core.types import Result

T = TypeVar("T")


class IQueryExecutor(ABC, Generic[T]):
    """Interface for query execution"""

    @abstractmethod
    async def execute(self, query: str, params: Optional[Dict] = None) -> Result[T]:
        """Execute query"""
        pass


class ITransactionManager(ABC):
    """Interface for transaction management"""

    @abstractmethod
    async def begin(self) -> AsyncSession:
        """Begin transaction"""
        pass

    @abstractmethod
    async def commit(self) -> None:
        """Commit transaction"""
        pass

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback transaction"""
        pass


class ICacheManager(ABC, Generic[T]):
    """Interface for cache management"""

    @abstractmethod
    def get(self, key: str) -> Optional[T]:
        """Get cached value"""
        pass

    @abstractmethod
    def set(self, key: str, value: T) -> None:
        """Set cache value"""
        pass

    @abstractmethod
    def invalidate(self, key: str) -> None:
        """Invalidate cache key"""
        pass


class IModelManager(ABC, Generic[T]):
    """Interface for model management"""

    @abstractmethod
    async def create(self, **data: object) -> Result[T]:
        """Create model instance"""
        pass

    @abstractmethod
    async def update(self, id: Union[int, str], **data: object) -> Result[T]:
        """Update model instance"""
        pass

    @abstractmethod
    async def delete(self, id: Union[int, str]) -> Result[bool]:
        """Delete model instance"""
        pass
