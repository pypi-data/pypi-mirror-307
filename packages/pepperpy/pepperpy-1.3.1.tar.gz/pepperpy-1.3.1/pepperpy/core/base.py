"""Core base classes and interfaces for PepperPy modules"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List, Optional

from .types import JsonDict, ModuleStatus


@dataclass
class ModuleConfig:
    """Enhanced base configuration for all modules"""

    enabled: bool = True
    debug: bool = False
    name: Optional[str] = None
    version: str = "1.0.0"
    strict_mode: bool = True
    auto_initialize: bool = True
    timeout: float = 30.0
    retry_attempts: int = 3
    retry_delay: float = 1.0
    metrics_enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseModule(ABC):
    """Base class for all PepperPy modules."""

    __module_name__: ClassVar[str]
    __dependencies__: ClassVar[List[str]] = []

    def __init__(self, config: Optional[ModuleConfig] = None):
        self.config = config or ModuleConfig()
        self._status = ModuleStatus.INACTIVE

    @abstractmethod
    async def setup(self) -> None:
        """Initialize module resources."""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup module resources."""
        pass

    @property
    def name(self) -> str:
        """Get module name."""
        return self.__module_name__

    @property
    def dependencies(self) -> List[str]:
        """Get module dependencies."""
        return self.__dependencies__

    def get_status(self) -> ModuleStatus:
        """Get current module status."""
        return self._status

    def get_metadata(self) -> JsonDict:
        """Get module metadata."""
        return {
            "name": self.name,
            "status": self._status.name,
            "version": self.config.version,
            **self.config.metadata,
        }
