import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Awaitable, Callable, Dict, List, Optional, TypeVar

from .types import Priority, ProcessingTask  # Importando do novo arquivo de tipos

T = TypeVar("T")
R = TypeVar("R")


class BatchProcessor:
    """Advanced batch processing with priorities and monitoring"""

    def __init__(
        self,
        max_concurrent: int = 3,
        max_batch_size: int = 20,
        executor: Optional[ThreadPoolExecutor] = None,
    ) -> None:
        self.max_concurrent = max_concurrent
        self.max_batch_size = max_batch_size
        self.executor = executor or ThreadPoolExecutor(max_workers=max_concurrent)
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._queues: Dict[Priority, asyncio.PriorityQueue] = {
            p: asyncio.PriorityQueue() for p in Priority
        }
        self._active_tasks: int = 0
        self._total_processed: int = 0

    async def process_batch(
        self,
        items: List[T],
        processor: Callable[[T], Awaitable[R]],
        priority: Priority = Priority.NORMAL,
        batch_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[R]:
        """Process items with priority"""
        tasks = [
            ProcessingTask(item=item, priority=priority, metadata=batch_metadata or {})
            for item in items
        ]

        # Add tasks to priority queue
        for task in tasks:
            await self._queues[task.priority].put(
                (-task.created_at, task)  # Negative for FIFO within priority
            )

        results = []

        # Process in batches respecting priority
        while len(results) < len(items):
            batch = await self._get_next_batch(min(self.max_batch_size, len(items) - len(results)))

            batch_results = await asyncio.gather(
                *(self._process_item(task.item, processor) for task in batch)
            )
            results.extend(batch_results)

        return results

    async def _get_next_batch(self, size: int) -> List[ProcessingTask]:
        """Get next batch of tasks respecting priorities"""
        batch = []

        while len(batch) < size:
            # Try each priority level
            for priority in reversed(Priority):
                if not self._queues[priority].empty():
                    _, task = await self._queues[priority].get()
                    batch.append(task)
                    break
            else:
                # No more tasks
                break

        return batch

    async def _process_item(self, item: T, processor: Callable[[T], Awaitable[R]]) -> R:
        """Process single item with monitoring"""
        async with self._semaphore:
            self._active_tasks += 1
            try:
                result = await processor(item)
                self._total_processed += 1
                return result
            finally:
                self._active_tasks -= 1

    @property
    def stats(self) -> Dict[str, Any]:
        """Get processor statistics"""
        return {
            "active_tasks": self._active_tasks,
            "total_processed": self._total_processed,
            "queue_sizes": {p.name: self._queues[p].qsize() for p in Priority},
        }
