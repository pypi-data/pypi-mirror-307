import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from pepperpy.core import BaseModule, ModuleConfig
from pepperpy.core.types import Serializable


@dataclass
class Context(Serializable):
    """Middleware execution context"""

    request_id: str
    timestamp: datetime
    data: Dict[str, Any]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Context":
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)


class MiddlewareModule(BaseModule):
    """Middleware chain management and execution"""

    __module_name__ = "middleware"
    __dependencies__ = ["metrics"]

    def __init__(self, config: Optional[ModuleConfig] = None):
        super().__init__(config or ModuleConfig())
        self._middleware: Dict[str, List[Callable]] = {}
        self._error_handlers: List[Callable] = []

    async def initialize(self) -> None:
        await super().initialize()

    def register(self, chain: str, middleware: Callable) -> None:
        """Register middleware in chain"""
        if chain not in self._middleware:
            self._middleware[chain] = []
        self._middleware[chain].append(middleware)

    def register_error_handler(self, handler: Callable) -> None:
        """Register error handler"""
        self._error_handlers.append(handler)

    async def execute(self, chain: str, context: Context) -> Context:
        """Execute middleware chain"""
        if chain not in self._middleware:
            return context

        start_time = datetime.now()

        try:
            current_context = context
            for middleware in self._middleware[chain]:
                try:
                    if asyncio.iscoroutinefunction(middleware):
                        current_context = await middleware(current_context)
                    else:
                        current_context = middleware(current_context)
                except Exception as e:
                    await self._handle_error(e, current_context)
                    raise

            return current_context
        finally:
            elapsed = (datetime.now() - start_time).total_seconds()
            await self.metrics.record("middleware.execution_time", elapsed, {"chain": chain})

    async def _handle_error(self, error: Exception, context: Context) -> None:
        """Execute error handlers"""
        for handler in self._error_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(error, context)
                else:
                    handler(error, context)
            except Exception as e:
                self._logger.error(f"Error in middleware error handler: {e}")
