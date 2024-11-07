from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class QueryMetrics:
    """Query performance metrics"""

    total_queries: int = 0
    total_duration: float = 0.0
    avg_duration: float = 0.0
    min_duration: float = float("inf")
    max_duration: float = 0.0
    queries_per_second: float = 0.0
    error_count: int = 0
    start_time: datetime = field(default_factory=datetime.utcnow)

    def record_query(self, duration: float, error: bool = False) -> None:
        """Record query metrics"""
        self.total_queries += 1
        if error:
            self.error_count += 1

        if not error:
            self.total_duration += duration
            self.min_duration = min(self.min_duration, duration)
            self.max_duration = max(self.max_duration, duration)
            self.avg_duration = self.total_duration / (self.total_queries - self.error_count)

            elapsed = (datetime.utcnow() - self.start_time).total_seconds()
            self.queries_per_second = (self.total_queries - self.error_count) / elapsed


@dataclass
class DatabaseMetrics:
    """Database performance metrics"""

    query_metrics: QueryMetrics = field(default_factory=QueryMetrics)
    connection_count: int = 0
    active_transactions: int = 0
    pool_size: int = 0
    pool_available: int = 0
    last_error: Optional[str] = None
    last_error_time: Optional[datetime] = None

    def record_error(self, error: Exception) -> None:
        """Record database error"""
        self.last_error = str(error)
        self.last_error_time = datetime.utcnow()

    def update_pool_stats(self, size: int, available: int) -> None:
        """Update connection pool statistics"""
        self.pool_size = size
        self.pool_available = available
