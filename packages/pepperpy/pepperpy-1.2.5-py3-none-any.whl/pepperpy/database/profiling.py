from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class QueryProfile:
    """Profile information for a single query"""

    query: str
    start_time: datetime
    end_time: Optional[datetime] = None
    params: Optional[Dict] = None
    rows_affected: int = 0
    cache_hit: bool = False
    retries: int = 0

    @property
    def duration(self) -> float:
        """Get query duration in seconds"""
        if not self.end_time:
            return 0.0
        return (self.end_time - self.start_time).total_seconds()


@dataclass
class DatabaseProfile:
    """Database performance profiling"""

    # Query statistics
    queries: List[QueryProfile] = field(default_factory=list)
    slow_threshold: float = 1.0  # seconds

    # Connection statistics
    total_connections: int = 0
    active_connections: int = 0
    idle_connections: int = 0

    # Cache statistics
    cache_hits: int = 0
    cache_misses: int = 0

    # Transaction statistics
    transactions_started: int = 0
    transactions_committed: int = 0
    transactions_rolled_back: int = 0

    def add_query(self, profile: QueryProfile) -> None:
        """Add query profile"""
        self.queries.append(profile)

        if profile.cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

    def get_slow_queries(self) -> List[QueryProfile]:
        """Get queries that exceeded slow threshold"""
        return [q for q in self.queries if q.duration > self.slow_threshold]

    def get_statistics(self) -> Dict[str, Any]:
        """Get profiling statistics"""
        total_queries = len(self.queries)
        total_duration = sum(q.duration for q in self.queries)
        avg_duration = total_duration / total_queries if total_queries > 0 else 0

        return {
            "total_queries": total_queries,
            "total_duration": total_duration,
            "average_duration": avg_duration,
            "slow_queries": len(self.get_slow_queries()),
            "cache_hit_ratio": (
                self.cache_hits / (self.cache_hits + self.cache_misses)
                if (self.cache_hits + self.cache_misses) > 0
                else 0
            ),
            "transaction_success_ratio": (
                self.transactions_committed / self.transactions_started
                if self.transactions_started > 0
                else 0
            ),
            "connection_utilization": (
                self.active_connections / self.total_connections
                if self.total_connections > 0
                else 0
            ),
        }


class DatabaseProfiler:
    """Database operation profiler"""

    def __init__(self, slow_threshold: float = 1.0) -> None:
        self._profile = DatabaseProfile(slow_threshold=slow_threshold)
        self._start_time = datetime.utcnow()

    def start_query(self, query: str, params: Optional[Dict] = None) -> QueryProfile:
        """Start profiling a query"""
        profile = QueryProfile(query=query, params=params, start_time=datetime.utcnow())
        return profile

    def end_query(self, profile: QueryProfile, rows_affected: int = 0) -> None:
        """End query profiling"""
        profile.end_time = datetime.utcnow()
        profile.rows_affected = rows_affected
        self._profile.add_query(profile)

    def record_cache_hit(self, query: str) -> None:
        """Record cache hit"""
        profile = QueryProfile(
            query=query,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow(),
            cache_hit=True,
        )
        self._profile.add_query(profile)

    def record_transaction(self, committed: bool) -> None:
        """Record transaction result"""
        self._profile.transactions_started += 1
        if committed:
            self._profile.transactions_committed += 1
        else:
            self._profile.transactions_rolled_back += 1

    def update_connection_stats(self, total: int, active: int, idle: int) -> None:
        """Update connection statistics"""
        self._profile.total_connections = total
        self._profile.active_connections = active
        self._profile.idle_connections = idle

    def get_profile(self) -> DatabaseProfile:
        """Get current profile"""
        return self._profile

    def reset(self) -> None:
        """Reset profiling data"""
        self._profile = DatabaseProfile(slow_threshold=self._profile.slow_threshold)
        self._start_time = datetime.utcnow()
