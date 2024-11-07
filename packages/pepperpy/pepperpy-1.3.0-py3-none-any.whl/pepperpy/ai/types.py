from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict


class Priority(Enum):
    """Task priority levels"""

    LOW = 0
    NORMAL = 1
    HIGH = 2


@dataclass
class ProcessingTask:
    """Task with priority and metadata"""

    item: Any
    priority: Priority
    metadata: Dict[str, Any]
    created_at: float
