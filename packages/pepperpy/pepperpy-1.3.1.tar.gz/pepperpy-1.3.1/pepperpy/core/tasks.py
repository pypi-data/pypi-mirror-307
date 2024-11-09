"""Task management and scheduling system"""

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional

from .base import BaseModule, ModuleConfig
from .metrics import Metric, MetricType
from .types import JsonDict


class TaskStatus(Enum):
    """Task execution status"""

    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


@dataclass
class TaskConfig(ModuleConfig):
    """Task system configuration"""

    max_concurrent: int = 10
    default_timeout: float = 300.0  # 5 minutes
    retry_limit: int = 3
    retry_delay: float = 5.0
    preserve_completed: bool = False
    auto_cleanup: bool = True


@dataclass
class Task:
    """Task definition and metadata"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = field(default="unnamed_task")
    func: Callable = field(repr=False)
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    status: TaskStatus = field(default=TaskStatus.PENDING)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    retries: int = 0
    timeout: Optional[float] = None
    result: Any = None

    def to_dict(self) -> JsonDict:
        """Convert task to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.name,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error": self.error,
            "retries": self.retries,
        }


class TaskManager(BaseModule):
    """Enhanced task management system"""

    __module_name__ = "tasks"
    __dependencies__ = ["metrics"]

    def __init__(self, config: Optional[TaskConfig] = None) -> None:
        super().__init__(config or TaskConfig())
        self._tasks: Dict[str, Task] = {}
        self._running_tasks: Dict[str, asyncio.Task] = {}
        self._semaphore = asyncio.Semaphore(self.config.max_concurrent)
        self._cleanup_task: Optional[asyncio.Task] = None

    async def initialize(self) -> None:
        """Initialize task system"""
        await super().initialize()
        if self.config.auto_cleanup:
            self._cleanup_task = asyncio.create_task(self._periodic_cleanup())

    async def cleanup(self) -> None:
        """Cleanup task system"""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

        # Cancel all running tasks
        for task in self._running_tasks.values():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        self._tasks.clear()
        self._running_tasks.clear()
        await super().cleanup()

    async def submit(self, func: Callable, *args: Any, **kwargs: Any) -> Task:
        """Submit new task for execution"""
        name = kwargs.pop("name", func.__name__)
        timeout = kwargs.pop("timeout", self.config.default_timeout)

        task = Task(name=name, func=func, args=args, kwargs=kwargs, timeout=timeout)

        self._tasks[task.id] = task
        asyncio_task = asyncio.create_task(self._execute_task(task))
        self._running_tasks[task.id] = asyncio_task

        return task

    async def cancel(self, task_id: str) -> None:
        """Cancel running task"""
        if task_id in self._running_tasks:
            self._running_tasks[task_id].cancel()
            self._tasks[task_id].status = TaskStatus.CANCELLED

    async def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return self._tasks.get(task_id)

    async def get_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """Get all tasks, optionally filtered by status"""
        if status:
            return [t for t in self._tasks.values() if t.status == status]
        return list(self._tasks.values())

    async def _execute_task(self, task: Task) -> None:
        """Execute single task with retries"""
        async with self._semaphore:
            task.started_at = datetime.now()
            task.status = TaskStatus.RUNNING

            while task.retries <= self.config.retry_limit:
                try:
                    if asyncio.iscoroutinefunction(task.func):
                        task.result = await asyncio.wait_for(
                            task.func(*task.args, **task.kwargs), timeout=task.timeout
                        )
                    else:
                        task.result = await asyncio.get_event_loop().run_in_executor(
                            None, task.func, *task.args, **task.kwargs
                        )

                    task.status = TaskStatus.COMPLETED
                    task.completed_at = datetime.now()
                    await self._record_metrics(task)
                    break

                except asyncio.TimeoutError:
                    task.error = "Task timed out"
                    task.status = TaskStatus.FAILED

                except Exception as e:
                    task.error = str(e)
                    task.retries += 1

                    if task.retries <= self.config.retry_limit:
                        await asyncio.sleep(self.config.retry_delay)
                        continue

                    task.status = TaskStatus.FAILED

            if task.id in self._running_tasks:
                del self._running_tasks[task.id]

    async def _periodic_cleanup(self) -> None:
        """Periodically clean up completed tasks"""
        while True:
            try:
                await asyncio.sleep(300)  # Clean every 5 minutes
                await self._cleanup_completed()
            except asyncio.CancelledError:
                break

    async def _cleanup_completed(self) -> None:
        """Clean up completed tasks"""
        if not self.config.preserve_completed:
            self._tasks = {
                tid: task
                for tid, task in self._tasks.items()
                if task.status not in (TaskStatus.COMPLETED, TaskStatus.CANCELLED)
            }

    async def _record_metrics(self, task: Task) -> None:
        """Record task metrics"""
        if not task.completed_at or not task.started_at:
            return

        duration = (task.completed_at - task.started_at).total_seconds()

        metrics = [
            Metric(
                name="task_duration",
                value=duration,
                type=MetricType.HISTOGRAM,
                labels={"task_name": task.name},
            ),
            Metric(
                name="task_retries",
                value=task.retries,
                type=MetricType.COUNTER,
                labels={"task_name": task.name},
            ),
        ]

        for metric in metrics:
            await self.metrics.record(metric)
