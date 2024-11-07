import asyncio
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


@dataclass
class SchedulerConfig:
    """Configuration for dynamic scheduler"""

    max_batch_size: int = 32
    min_batch_size: int = 4
    target_latency: float = 0.1  # seconds
    adjustment_factor: float = 0.1
    warmup_batches: int = 100
    max_queue_size: int = 1000
    priority_levels: int = 3


class DynamicBatchScheduler:
    """Dynamic batch scheduler with priority queues"""

    def __init__(self, config: SchedulerConfig):
        self.config = config

        # Initialize queues for different priorities
        self.queues = [
            asyncio.PriorityQueue(maxsize=config.max_queue_size)
            for _ in range(config.priority_levels)
        ]

        # Statistics for dynamic adjustment
        self.batch_stats = {"sizes": [], "latencies": [], "throughputs": []}

        self.current_batch_size = config.min_batch_size
        self._stop = False

    async def add_request(
        self, priority: int, request: Any, deadline: Optional[float] = None
    ) -> None:
        """Add request to appropriate priority queue"""
        if priority >= self.config.priority_levels:
            priority = self.config.priority_levels - 1

        # Use current time as priority if no deadline
        if deadline is None:
            deadline = time.time()

        await self.queues[priority].put((deadline, request))

    async def get_batch(self) -> Tuple[List[Any], List[float]]:
        """Get batch of requests respecting priorities"""
        batch = []
        deadlines = []

        # Try to fill batch starting from highest priority
        start_time = time.time()
        while len(batch) < self.current_batch_size and not self._stop:
            # Check each priority queue
            for queue in self.queues:
                while len(batch) < self.current_batch_size and not queue.empty():
                    deadline, request = await queue.get()

                    # Skip if deadline passed
                    if deadline < start_time:
                        continue

                    batch.append(request)
                    deadlines.append(deadline)

            # Break if we have minimum batch size
            if len(batch) >= self.config.min_batch_size:
                break

            # Small delay before checking again
            await asyncio.sleep(0.001)

        return batch, deadlines

    def update_stats(self, batch_size: int, latency: float) -> None:
        """Update statistics and adjust batch size"""
        self.batch_stats["sizes"].append(batch_size)
        self.batch_stats["latencies"].append(latency)

        # Calculate throughput
        throughput = batch_size / latency
        self.batch_stats["throughputs"].append(throughput)

        # Only adjust after warmup
        if len(self.batch_stats["sizes"]) < self.config.warmup_batches:
            return

        # Get recent statistics
        recent_latencies = self.batch_stats["latencies"][-50:]
        avg_latency = np.mean(recent_latencies)

        # Adjust batch size
        if avg_latency > self.config.target_latency:
            # Reduce batch size
            self.current_batch_size = max(
                self.config.min_batch_size,
                int(self.current_batch_size * (1 - self.config.adjustment_factor)),
            )
        else:
            # Increase batch size
            self.current_batch_size = min(
                self.config.max_batch_size,
                int(self.current_batch_size * (1 + self.config.adjustment_factor)),
            )

    def get_stats(self) -> Dict[str, Any]:
        """Get scheduler statistics"""
        if not self.batch_stats["sizes"]:
            return {}

        return {
            "avg_batch_size": np.mean(self.batch_stats["sizes"]),
            "avg_latency": np.mean(self.batch_stats["latencies"]),
            "avg_throughput": np.mean(self.batch_stats["throughputs"]),
            "current_batch_size": self.current_batch_size,
            "queue_sizes": [q.qsize() for q in self.queues],
        }

    def stop(self) -> None:
        """Stop the scheduler"""
        self._stop = True
