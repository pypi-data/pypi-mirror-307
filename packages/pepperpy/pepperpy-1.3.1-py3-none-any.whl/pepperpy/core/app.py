"""Core application class and lifecycle management"""

import asyncio
import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, AsyncIterator, Dict, List, Optional, Type

from .base import BaseModule, ModuleConfig
from .events import EventBus
from .exceptions import ApplicationError
from .hooks import HookManager
from .metrics import MetricsModule
from .types import JsonDict


class AppStatus(Enum):
    """Application lifecycle status"""

    CREATED = auto()
    INITIALIZING = auto()
    RUNNING = auto()
    SHUTTING_DOWN = auto()
    ERROR = auto()


@dataclass
class AppConfig(ModuleConfig):
    """Application configuration"""

    name: str = "PepperPy App"
    debug: bool = False
    strict_mode: bool = True
    shutdown_timeout: float = 30.0
    module_timeout: float = 10.0
    metrics_enabled: bool = True
    auto_recovery: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


class Application:
    """Enhanced PepperPy application manager"""

    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or AppConfig()
        self._modules: Dict[str, BaseModule] = {}
        self._logger = logging.getLogger(f"pepperpy.app.{self.config.name}")
        self._status = AppStatus.CREATED
        self._start_time = datetime.now()
        self._lock = asyncio.Lock()
        self._error: Optional[Exception] = None

        # Core systems
        self.events = EventBus()
        self.metrics = MetricsModule()
        self.hooks = HookManager()

    async def initialize(self) -> None:
        """Initialize application and all modules"""
        if self._status != AppStatus.CREATED:
            return

        try:
            async with self._lock:
                self._status = AppStatus.INITIALIZING
                self._logger.info(f"Initializing application: {self.config.name}")

                # Initialize core systems
                await self._initialize_core_systems()

                # Initialize modules in dependency order
                modules = self._resolve_dependencies()
                for module in modules:
                    await self._initialize_module(module)

                self._status = AppStatus.RUNNING
                await self._record_metric("app_initialized")

        except Exception as e:
            self._error = e
            self._status = AppStatus.ERROR
            self._logger.error(f"Application initialization failed: {e}")
            raise ApplicationError(f"Failed to initialize application: {e}") from e

    async def cleanup(self) -> None:
        """Cleanup application and all modules"""
        if self._status not in (AppStatus.RUNNING, AppStatus.ERROR):
            return

        try:
            async with self._lock:
                self._status = AppStatus.SHUTTING_DOWN
                self._logger.info(f"Cleaning up application: {self.config.name}")

                # Cleanup modules in reverse dependency order
                modules = reversed(self._resolve_dependencies())
                await asyncio.gather(
                    *[self._cleanup_module(m) for m in modules], return_exceptions=True
                )

                # Cleanup core systems
                await self._cleanup_core_systems()

                self._status = AppStatus.CREATED
                await self._record_metric("app_cleaned_up")

        except Exception as e:
            self._error = e
            self._status = AppStatus.ERROR
            self._logger.error(f"Application cleanup failed: {e}")
            raise ApplicationError(f"Failed to cleanup application: {e}") from e

    @asynccontextmanager
    async def run(self) -> AsyncIterator["Application"]:
        """Context manager for running the application

        Returns:
            AsyncIterator[Application]: The application instance
        """
        try:
            await self.initialize()
            yield self
        finally:
            await self.cleanup()

    def register_module(
        self, module_class: Type[BaseModule], config: Optional[ModuleConfig] = None
    ) -> BaseModule:
        """Register module with application"""
        name = module_class.__module_name__
        if name in self._modules:
            raise ApplicationError(f"Module already registered: {name}")

        module = module_class(config)
        self._modules[name] = module

        return module

    def get_module(self, name: str) -> Optional[BaseModule]:
        """Get module by name"""
        return self._modules.get(name)

    def get_status(self) -> AppStatus:
        """Get current application status"""
        return self._status

    def get_metadata(self) -> JsonDict:
        """Get application metadata"""
        return {
            "name": self.config.name,
            "status": self._status.name,
            "uptime": (datetime.now() - self._start_time).total_seconds(),
            "modules": list(self._modules.keys()),
            "error": str(self._error) if self._error else None,
            **self.config.metadata,
        }

    async def _initialize_core_systems(self) -> None:
        """Initialize core application systems"""
        await self.events.initialize()
        if self.config.metrics_enabled:
            await self.metrics.initialize()
        await self.hooks.initialize()

    async def _cleanup_core_systems(self) -> None:
        """Cleanup core application systems"""
        if self.config.metrics_enabled:
            await self.metrics.cleanup()
        await self.hooks.cleanup()
        await self.events.cleanup()

    async def _initialize_module(self, module: BaseModule) -> None:
        """Initialize single module with timeout"""
        try:
            async with asyncio.timeout(self.config.module_timeout):
                await module.initialize()
        except Exception as e:
            self._logger.error(f"Failed to initialize module {module.__module_name__}: {e}")
            if self.config.strict_mode:
                raise

    async def _cleanup_module(self, module: BaseModule) -> None:
        """Cleanup single module with timeout"""
        try:
            async with asyncio.timeout(self.config.module_timeout):
                await module.cleanup()
        except Exception as e:
            self._logger.error(f"Failed to cleanup module {module.__module_name__}: {e}")

    async def _record_metric(self, name: str) -> None:
        """Record application metric"""
        if self.config.metrics_enabled and self.metrics:
            await self.metrics.record_metric(
                name=f"app_{name}", value=1, labels={"app": self.config.name}
            )

    def _resolve_dependencies(self) -> List[BaseModule]:
        """Resolve module dependencies with cycle detection"""
        resolved = []
        visiting = set()

        def visit(module: BaseModule):
            name = module.__module_name__
            if name in visiting:
                raise ApplicationError(f"Circular dependency detected: {name}")
            if module in resolved:
                return

            visiting.add(name)

            for dep in module.__dependencies__:
                if dep not in self._modules:
                    raise ApplicationError(f"Missing dependency {dep} for module {name}")
                visit(self._modules[dep])

            visiting.remove(name)
            resolved.append(module)

        for module in self._modules.values():
            visit(module)

        return resolved
