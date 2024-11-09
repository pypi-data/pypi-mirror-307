"""Base processor for storage operations"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol

from pepperpy.core.types import PathLike


class ProcessorProtocol(Protocol):
    """Protocol for storage processors"""

    async def process(
        self,
        source: PathLike,
        operations: Optional[List[Dict[str, Any]]] = None,
        output_format: Optional[str] = None,
    ) -> Path: ...


class BaseProcessor(ABC):
    """Base class for all storage processors"""

    def __init__(self, config: Any):
        self.config = config

    @abstractmethod
    async def process(
        self,
        source: PathLike,
        operations: Optional[List[Dict[str, Any]]] = None,
        output_format: Optional[str] = None,
    ) -> Path:
        """Process file with operations"""
        raise NotImplementedError

    @abstractmethod
    async def get_metadata(self, path: PathLike) -> Dict[str, Any]:
        """Get file metadata"""
        raise NotImplementedError
