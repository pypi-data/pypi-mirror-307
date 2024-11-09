"""Enhanced event system with priority and async support"""

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Protocol, TypeVar

from .base import BaseModule, ModuleConfig
from .exceptions import EventError
from .types import JsonDict

T = TypeVar("T")


class EventPriority(Enum):
    """Event handler priority levels"""

    LOW = auto()
    NORMAL = auto()
    HIGH = auto()
    CRITICAL = auto()


@dataclass
class EventConfig(ModuleConfig):
    """Event system configuration"""

    max_handlers: int = 100
    enable_async: bool = True
    strict_mode: bool = True
    preserve_order: bool = True
    error_handling: str = "log"  # log, raise, ignore


@dataclass
class Event:
    """Enhanced event data structure"""

    name: str
    data: Any
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    source: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> JsonDict:
        """Convert event to dictionary format"""
        return {
            "id": self.id,
            "name": self.name,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "metadata": self.metadata,
        }


@dataclass
class EventHandler:
    """Event handler registration"""

    callback: Callable
    priority: EventPriority = EventPriority.NORMAL
    async_handler: bool = False
    filter_fn: Optional[Callable[[Event], bool]] = None


class EventBusProtocol(Protocol):
    """Protocol for event bus implementations"""

    async def publish(self, event: Event) -> None: ...
    async def subscribe(
        self, event_name: str, handler: Callable, priority: EventPriority = EventPriority.NORMAL
    ) -> None: ...
    async def unsubscribe(self, event_name: str, handler: Callable) -> None: ...


class EventBus(BaseModule):
    """Enhanced event management system"""

    __module_name__ = "events"
    __dependencies__ = ["metrics"]

    def __init__(self, config: Optional[EventConfig] = None) -> None:
        super().__init__(config or EventConfig())
        self._handlers: Dict[str, List[EventHandler]] = {}
        self._lock = asyncio.Lock()
        self._metrics = None

    async def initialize(self) -> None:
        """Initialize event system"""
        await super().initialize()
        self._metrics = self.get_module("metrics")

    async def cleanup(self) -> None:
        """Cleanup event system"""
        async with self._lock:
            self._handlers.clear()
        await super().cleanup()

    async def subscribe(
        self,
        event_name: str,
        handler: Callable,
        priority: EventPriority = EventPriority.NORMAL,
        filter_fn: Optional[Callable[[Event], bool]] = None,
    ) -> None:
        """
        Subscribe to an event with priority and filtering

        Args:
            event_name: Name of the event to subscribe to
            handler: Callback function to handle the event
            priority: Handler priority level
            filter_fn: Optional function to filter events
        """
        if len(self._handlers.get(event_name, [])) >= self.config.max_handlers:
            raise EventError(f"Maximum handlers reached for event: {event_name}")

        async with self._lock:
            if event_name not in self._handlers:
                self._handlers[event_name] = []

            event_handler = EventHandler(
                callback=handler,
                priority=priority,
                async_handler=asyncio.iscoroutinefunction(handler),
                filter_fn=filter_fn,
            )

            self._handlers[event_name].append(event_handler)
            if self.config.preserve_order:
                self._sort_handlers(event_name)

    async def unsubscribe(self, event_name: str, handler: Callable) -> None:
        """Unsubscribe handler from event"""
        async with self._lock:
            if event_name in self._handlers:
                self._handlers[event_name] = [
                    h for h in self._handlers[event_name] if h.callback != handler
                ]

    async def publish(self, event: Event) -> None:
        """
        Publish event to all subscribers

        Args:
            event: Event to publish
        """
        handlers = self._handlers.get(event.name, [])

        for handler in handlers:
            if handler.filter_fn and not handler.filter_fn(event):
                continue

            try:
                if handler.async_handler:
                    await handler.callback(event)
                else:
                    handler.callback(event)

                if self._metrics:
                    await self._record_metrics(event, handler)

            except Exception as e:
                error_msg = f"Error in event handler: {e}"
                if self.config.error_handling == "raise":
                    raise EventError(error_msg) from e
                elif self.config.error_handling == "log":
                    self._logger.error(error_msg)

    def _sort_handlers(self, event_name: str) -> None:
        """Sort handlers by priority"""
        self._handlers[event_name].sort(key=lambda h: h.priority.value, reverse=True)

    async def _record_metrics(self, event: Event, handler: EventHandler) -> None:
        """Record event metrics"""
        await self._metrics.record_metric(
            name="event_processed",
            value=1,
            labels={
                "event": event.name,
                "priority": handler.priority.name,
                "async": str(handler.async_handler),
            },
        )

    async def _dispatch_event(self, event: Event) -> None:
        """Dispatch event to handlers"""
        handlers = self._handlers.get(event.name, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                error_msg = f"Error in event handler: {e}"
                if self.config.error_handling == "raise":
                    raise EventError(error_msg) from e
                elif self.config.error_handling == "log":
                    self._logger.error(error_msg)
