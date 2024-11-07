from typing import Generic, Type, TypeVar

from sqlalchemy import Select, and_, select
from sqlalchemy.sql import Executable

from .models import BaseModel

T = TypeVar("T", bound=BaseModel)


class QueryBuilder(Generic[T]):
    """Advanced query builder with type support"""

    def __init__(self, model_class: Type[T]) -> None:
        self.model_class = model_class
        self._query: Select = select(model_class)
        self._conditions = []

    def filter(self, *conditions: object) -> "QueryBuilder[T]":
        """Add filter conditions"""
        self._conditions.extend(conditions)
        return self

    def filter_by(self, **kwargs: object) -> "QueryBuilder[T]":
        """Add equality conditions"""
        conditions = [getattr(self.model_class, key) == value for key, value in kwargs.items()]
        return self.filter(*conditions)

    def order_by(self, *criteria: object) -> "QueryBuilder[T]":
        """Add ordering criteria"""
        self._query = self._query.order_by(*criteria)
        return self

    def limit(self, limit: int) -> "QueryBuilder[T]":
        """Set result limit"""
        self._query = self._query.limit(limit)
        return self

    def offset(self, offset: int) -> "QueryBuilder[T]":
        """Set result offset"""
        self._query = self._query.offset(offset)
        return self

    def build(self) -> Executable:
        """Build final query"""
        if self._conditions:
            self._query = self._query.where(and_(*self._conditions))
        return self._query

    @classmethod
    def for_model(cls, model: Type[T]) -> "QueryBuilder[T]":
        """Create query builder for model"""
        return cls(model)
