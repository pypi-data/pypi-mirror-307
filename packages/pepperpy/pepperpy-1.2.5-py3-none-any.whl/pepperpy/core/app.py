import asyncio
import signal
import types
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, List, Optional, Type, TypeVar

from .config import Config, ConfigProvider
from .context import Context
from .events import Event, EventBus, SystemEvents
from .exceptions import (
    ApplicationStartupError,
    DependencyError,
    ValidationError,
)
from .health import HealthCheck, HealthMonitor, HealthStatus
from .logging import get_logger
from .module import Module

T = TypeVar("T", bound=Module)


class Application:
    """Aplicação principal"""

    def __init__(
        self,
        name: str,
        config_provider: Optional[ConfigProvider] = None,
        debug: bool = False,
    ) -> None:
        self.name = name
        self.debug = debug
        self.logger = get_logger("app")

        # Core components
        self._modules: Dict[str, Module] = {}
        self._event_bus = EventBus()
        self._context = Context()
        self._config = Config(config_provider)
        self._health = HealthMonitor()

        # State
        self._initialized = False
        self._shutting_down = False
        self._shutdown_task: Optional[asyncio.Task] = None

        # Setup signal handlers
        self._setup_signal_handlers()

    def _setup_signal_handlers(self) -> None:
        """Configura handlers de sinais"""
        for sig in (signal.SIGTERM, signal.SIGINT):
            signal.signal(sig, self._handle_shutdown_signal)

    def _handle_shutdown_signal(self, signum: int, frame: Optional[types.FrameType]) -> None:
        """Handler para sinais de shutdown"""
        if not self._shutting_down:
            self.logger.info("Shutdown signal received")
            self._shutting_down = True
            self._shutdown_task = asyncio.create_task(self._shutdown())

    def register_module(self, module: Module) -> "Application":
        """Registra um módulo"""
        module._set_event_bus(self._event_bus)
        module._set_context(self._context)

        with self.logger.context(module=module.name):
            self.logger.info("Registering module")

            # Apply configuration
            config = self._config.get(f"modules.{module.name}", {})
            module.config.settings.update(config)

            # Validate
            if module._validator:
                errors = module._validator.validate(module.config.settings)
                if errors:
                    raise ValidationError(f"Invalid configuration: {errors}")

            self._modules[module.name] = module
            self.logger.info("Module registered")

        return self

    def get_module(self, name: str, expected_type: Optional[Type[T]] = None) -> T:
        """Obtém um módulo"""
        module = self._modules.get(name)
        if not module:
            raise KeyError(f"Module '{name}' not found")

        if expected_type and not isinstance(module, expected_type):
            raise TypeError(f"Module '{name}' is not of type {expected_type}")

        return module

    async def _start(self) -> None:
        """Inicia a aplicação"""
        if self._initialized:
            return

        try:
            self.logger.info("Starting application")
            await self._event_bus.publish(Event(SystemEvents.STARTUP, "app"))

            # Validate dependencies
            self._validate_dependencies()

            # Initialize modules
            for module in self._get_initialization_order():
                if module.config.enabled:
                    self.logger.info(f"Initializing module: {module.name}")
                    await module.initialize()

            self._initialized = True
            self.logger.info("Application started")
            await self._event_bus.publish(Event(SystemEvents.STARTUP, "app"))

        except Exception as e:
            self.logger.error(f"Startup error: {e!s}")
            await self._shutdown()
            raise ApplicationStartupError(str(e)) from e

    async def _shutdown(self) -> None:
        """Finaliza a aplicação"""
        if not self._initialized or self._shutting_down:
            return

        self._shutting_down = True
        self.logger.info("Shutting down application")

        try:
            await self._event_bus.publish(Event(SystemEvents.SHUTDOWN, "app"))

            # Shutdown modules in reverse order
            for module in reversed(self._get_initialization_order()):
                if module._initialized:
                    self.logger.info(f"Shutting down module: {module.name}")
                    await module.shutdown()

            self._initialized = False
            self.logger.info("Application stopped")

        except Exception as e:
            self.logger.error(f"Shutdown error: {e!s}")
            raise

    def _validate_dependencies(self) -> None:
        """Valida dependências entre módulos"""
        for name, module in self._modules.items():
            for dep in module.__dependencies__:
                if dep not in self._modules:
                    raise DependencyError(
                        f"Module '{name}' depends on '{dep}' which is not registered"
                    )

    def _get_initialization_order(self) -> List[Module]:
        """Determina ordem de inicialização dos módulos"""
        visited = set()
        order = []

        def visit(name: str) -> None:
            if name in visited:
                return
            module = self._modules[name]
            for dep in module.__dependencies__:
                visit(dep)
            visited.add(name)
            order.append(module)

        for name in self._modules:
            visit(name)

        return order

    @asynccontextmanager
    async def run(self) -> AsyncIterator["Application"]:
        """Contexto de execução da aplicação"""
        await self._start()
        try:
            yield self
        finally:
            await self._shutdown()

    async def check_health(self) -> HealthCheck:
        """Verifica saúde do sistema"""
        checks = {}

        for name, module in self._modules.items():
            if module.config.enabled:
                try:
                    check = await module.check_health()
                    checks[name] = check
                except Exception as e:
                    checks[name] = HealthCheck(status=HealthStatus.UNHEALTHY, message=str(e))

        return HealthCheck(
            status=self._health.status,
            message=f"Application is {self._health.status}",
            checks=checks,
        )
