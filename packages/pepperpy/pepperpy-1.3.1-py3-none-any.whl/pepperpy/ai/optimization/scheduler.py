import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass
class SchedulerConfig:
    """Configuration for batch scheduler"""

    batch_size: int = 32
    max_concurrent: int = 3
    max_wait_time: float = 1.0
    min_batch_size: int = 1


class DynamicBatchScheduler:
    """Manages dynamic batching of requests"""

    def __init__(self, config: SchedulerConfig):
        self.config = config
        self._queue: asyncio.Queue = asyncio.Queue()
        self._stats: Dict[str, float] = {}

    async def add_request(self, priority: int, request: Dict[str, Any]) -> None:
        """Add request to scheduler queue"""
        await self._queue.put((priority, request))

    async def get_batch(self) -> Tuple[List[Dict[str, Any]], List[int]]:
        """Get next batch of requests"""
        batch = []
        priorities = []

        try:
            priority, request = await self._queue.get()
            batch.append(request)
            priorities.append(priority)

            while len(batch) < self.config.batch_size and not self._queue.empty():
                priority, request = await self._queue.get_nowait()
                batch.append(request)
                priorities.append(priority)

        except asyncio.QueueEmpty:
            pass

        return batch, priorities

    def update_stats(self, batch_size: int, latency: float) -> None:
        """Update scheduler statistics"""
        self._stats["avg_batch_size"] = batch_size
        self._stats["avg_latency"] = latency

    def stop(self) -> None:
        """Stop the scheduler"""
        # Cleanup if needed
        pass
