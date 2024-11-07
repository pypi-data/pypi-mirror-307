from abc import ABC, abstractmethod
from typing import Any, ClassVar, Dict, List, Optional, TypeVar

from pepperpy.core.health import HealthStatus
from pepperpy.core.metadata import ModuleMetadata

from .context import Context
from .events import EventBus
from .logging import get_logger
from .types import Status

T = TypeVar("T", bound="Module")


class Module(ABC):
    """Base class for all PepperPy modules with enhanced lifecycle management"""

    # Atributos de classe
    __module_name__: ClassVar[str]
    __version__: ClassVar[str]
    __description__: ClassVar[str]
    __dependencies__: ClassVar[List[str]]

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self._config = self._validate_config(config or {})
        self._status = Status.INACTIVE
        self._metadata = ModuleMetadata(
            name=self.__module_name__,
            version=self.__version__,
            description=self.__description__,
            dependencies=self.__dependencies__,
        )
        self._logger = get_logger(self.__module_name__)
        self._event_bus = EventBus()
        self._context = Context()

    def _validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate module configuration.

        Args:
            config: Configuration dictionary to validate

        Returns:
            The validated configuration dictionary

        Raises:
            ValueError: If configuration is invalid
        """
        # Default implementation accepts any config
        # Subclasses should override to add specific validation
        return config

    @abstractmethod
    async def setup(self) -> None:
        """Initialize module resources"""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup module resources"""
        pass

    async def health_check(self) -> HealthStatus:
        """Perform module health check"""
        return HealthStatus(
            module=self.__module_name__,
            state=self._status,
            details=self._get_health_details(),
        )

    def _get_health_details(self) -> Dict[str, Any]:
        """Get detailed health information"""
        return {
            "version": self.__version__,
            "status": self._status,
            "config": self._config,
        }
