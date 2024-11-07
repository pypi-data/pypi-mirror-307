from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar

from pepperpy.core.types import Result

T = TypeVar("T")


@dataclass
class QueryResult(Result[T], Generic[T]):
    """Enhanced query result with metadata"""

    query: str
    params: Optional[Dict[str, Any]] = None
    execution_time: float = 0.0

    rows_affected: int = 0
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class BatchResult(Result[List[T]], Generic[T]):
    """Result for batch operations"""

    total: int = 0
    succeeded: int = 0
    failed: int = 0
    errors: List[Dict[str, Any]] = None

    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        return self.succeeded / self.total if self.total > 0 else 0.0


@dataclass
class TransactionResult(Result[Any]):
    """Result for transaction operations"""

    transaction_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    operations: List[QueryResult] = None

    @property
    def duration(self) -> float:
        """Calculate transaction duration"""
        if not self.end_time:
            return 0.0
        return (self.end_time - self.start_time).total_seconds()
