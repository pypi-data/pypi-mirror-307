"""Enhanced plugin and extension hook system"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Protocol, TypeVar

from .base import BaseModule, ModuleConfig
from .exceptions import HookError
from .metrics import Metric, MetricType

T = TypeVar("T")


class HookType(Enum):
    """Hook execution types"""

    PRE = auto()  # Execute before main operation
    POST = auto()  # Execute after main operation
    ERROR = auto()  # Execute on error
    FILTER = auto()  # Modify data in pipeline


@dataclass
class HookConfig(ModuleConfig):
    """Hook system configuration"""

    parallel_execution: bool = False
    error_handling: str = "log"  # log, raise, ignore
    timeout: float = 30.0
    max_retries: int = 3
    preserve_order: bool = True


@dataclass
class Hook:
    """Enhanced hook registration"""

    name: str
    callback: Callable[..., Any]
    type: HookType
    priority: int = 0
    module: Optional[str] = None
    timeout: Optional[float] = None
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


class HookResult(Protocol):
    """Protocol for hook execution results"""

    async def success(self) -> bool: ...
    async def get_result(self) -> Any: ...
    async def get_error(self) -> Optional[Exception]: ...


@dataclass
class DefaultHookResult:
    """Default implementation of hook result"""

    _success: bool = True
    _result: Any = None
    _error: Optional[Exception] = None

    async def success(self) -> bool:
        return self._success

    async def get_result(self) -> Any:
        return self._result

    async def get_error(self) -> Optional[Exception]:
        return self._error


class HookManager(BaseModule):
    """Enhanced hook management system"""

    __module_name__ = "hooks"
    __dependencies__ = ["metrics"]

    def __init__(self, config: Optional[HookConfig] = None) -> None:
        super().__init__(config or HookConfig())
        self._hooks: Dict[str, List[Hook]] = {}
        self._lock = asyncio.Lock()
        self._metrics = None

    async def initialize(self) -> None:
        """Initialize hook system"""
        await super().initialize()
        self._metrics = self.get_module("metrics")

    async def register(self, hook: Hook, replace_existing: bool = False) -> None:
        """
        Register a new hook

        Args:
            hook: Hook to register
            replace_existing: Whether to replace existing hooks
        """
        async with self._lock:
            if hook.name not in self._hooks:
                self._hooks[hook.name] = []
            elif replace_existing:
                self._hooks[hook.name] = [
                    h for h in self._hooks[hook.name] if h.module != hook.module
                ]

            self._hooks[hook.name].append(hook)

            if self.config.preserve_order:
                self._sort_hooks(hook.name)

            await self._record_metric("hook_registered", hook)

    async def execute(
        self, hook_name: str, hook_type: HookType, *args: Any, **kwargs: Any
    ) -> List[HookResult]:
        """
        Execute hooks with comprehensive error handling

        Args:
            hook_name: Name of hooks to execute
            hook_type: Type of hooks to execute
            *args: Positional arguments for hooks
            **kwargs: Keyword arguments for hooks

        Returns:
            List of hook execution results
        """
        results: List[HookResult] = []
        hooks = [h for h in self._hooks.get(hook_name, []) if h.type == hook_type and h.enabled]

        if not hooks:
            return results

        if self.config.parallel_execution:
            results = await self._execute_parallel(hooks, *args, **kwargs)
        else:
            results = await self._execute_sequential(hooks, *args, **kwargs)

        await self._record_metric("hooks_executed", hooks)
        return results

    async def _execute_sequential(
        self, hooks: List[Hook], *args: Any, **kwargs: Any
    ) -> List[HookResult]:
        """Execute hooks sequentially"""
        results = []
        for hook in hooks:
            result = await self._execute_single_hook(hook, *args, **kwargs)
            results.append(result)
        return results

    async def _execute_parallel(
        self, hooks: List[Hook], *args: Any, **kwargs: Any
    ) -> List[HookResult]:
        """Execute hooks in parallel"""
        tasks = [self._execute_single_hook(hook, *args, **kwargs) for hook in hooks]
        return await asyncio.gather(*tasks)

    async def _execute_single_hook(self, hook: Hook, *args: Any, **kwargs: Any) -> HookResult:
        """Execute single hook with timeout and retry"""
        timeout = hook.timeout or self.config.timeout
        result = DefaultHookResult()

        for attempt in range(self.config.max_retries):
            try:
                if asyncio.iscoroutinefunction(hook.callback):
                    result._result = await asyncio.wait_for(
                        hook.callback(*args, **kwargs), timeout=timeout
                    )
                else:
                    result._result = hook.callback(*args, **kwargs)
                return result

            except Exception as e:
                result._success = False
                result._error = e

                if attempt == self.config.max_retries - 1:
                    if self.config.error_handling == "raise":
                        raise HookError(f"Hook {hook.name} failed: {e}") from e
                    elif self.config.error_handling == "log":
                        self._logger.error(f"Hook {hook.name} failed: {e}")

                await asyncio.sleep(1 * (attempt + 1))

        return result

    def _sort_hooks(self, hook_name: str) -> None:
        """Sort hooks by priority"""
        self._hooks[hook_name].sort(key=lambda h: (-h.priority, h.created_at))

    async def _record_metric(self, name: str, hook_data: Any) -> None:
        """Record hook metrics"""
        if self._metrics:
            metric = Metric(
                name=f"hook_{name}",
                value=1,
                type=MetricType.COUNTER,
                labels={
                    "hook_name": getattr(hook_data, "name", "unknown"),
                    "hook_type": getattr(hook_data, "type", "unknown").name,
                    "module": getattr(hook_data, "module", "unknown"),
                },
            )
            await self._metrics.record(metric)
