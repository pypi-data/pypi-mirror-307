"""Core type definitions"""

from enum import Enum, auto
from typing import Any, Dict, Protocol, TypeVar

JsonDict = Dict[str, Any]
T = TypeVar("T")


class MetricType(Enum):
    """Types of metrics that can be collected"""

    COUNTER = auto()
    GAUGE = auto()
    HISTOGRAM = auto()
    SUMMARY = auto()


class ModuleStatus(Enum):
    """Module lifecycle status"""

    INACTIVE = auto()
    INITIALIZING = auto()
    ACTIVE = auto()
    ERROR = auto()
    SHUTTING_DOWN = auto()


class ModuleProtocol(Protocol):
    """Protocol defining module interface"""

    async def initialize(self) -> None: ...
    async def cleanup(self) -> None: ...
    def get_status(self) -> ModuleStatus: ...
    def get_metadata(self) -> JsonDict: ...
