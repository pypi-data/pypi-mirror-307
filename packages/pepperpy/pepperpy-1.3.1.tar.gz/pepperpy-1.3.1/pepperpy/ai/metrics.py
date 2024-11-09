import asyncio
import json
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class AIMetric:
    """AI operation metric"""

    operation: str
    duration: float
    tokens: int
    success: bool
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


class MetricsCollector:
    """Collects and manages AI metrics"""

    def __init__(self, max_history: int = 1000):
        self._metrics = deque(maxlen=max_history)
        self._lock = asyncio.Lock()

    async def add_metric(self, metric: AIMetric) -> None:
        """Add new metric"""
        async with self._lock:
            self._metrics.append(metric)

    def get_metrics(self, operation: Optional[str] = None) -> list[AIMetric]:
        """Get metrics with optional filtering"""
        if operation:
            return [m for m in self._metrics if m.operation == operation]
        return list(self._metrics)

    def get_stats(self) -> Dict[str, Any]:
        """Get aggregated statistics"""
        stats = {
            "total_operations": len(self._metrics),
            "success_rate": 0,
            "avg_duration": 0,
            "total_tokens": 0,
            "operations": {},
        }

        if not self._metrics:
            return stats

        success_count = sum(1 for m in self._metrics if m.success)
        stats["success_rate"] = success_count / len(self._metrics)
        stats["avg_duration"] = sum(m.duration for m in self._metrics) / len(self._metrics)
        stats["total_tokens"] = sum(m.tokens for m in self._metrics)

        # Per operation stats
        op_stats: Dict[str, Dict[str, Any]] = {}
        for metric in self._metrics:
            if metric.operation not in op_stats:
                op_stats[metric.operation] = {
                    "count": 0,
                    "success": 0,
                    "total_duration": 0,
                    "total_tokens": 0,
                }

            stats = op_stats[metric.operation]
            stats["count"] += 1
            stats["success"] += 1 if metric.success else 0
            stats["total_duration"] += metric.duration
            stats["total_tokens"] += metric.tokens

        # Calculate averages
        for stats in op_stats.values():
            stats["success_rate"] = stats["success"] / stats["count"]
            stats["avg_duration"] = stats["total_duration"] / stats["count"]
            stats["avg_tokens"] = stats["total_tokens"] / stats["count"]

        stats["operations"] = op_stats
        return stats

    def export_metrics(self, path: str) -> None:
        """Export metrics to JSON file"""
        data = [
            {
                "operation": m.operation,
                "duration": m.duration,
                "tokens": m.tokens,
                "success": m.success,
                "metadata": m.metadata,
                "timestamp": m.timestamp.isoformat(),
            }
            for m in self._metrics
        ]

        with open(path, "w") as f:
            json.dump(data, f, indent=2)
