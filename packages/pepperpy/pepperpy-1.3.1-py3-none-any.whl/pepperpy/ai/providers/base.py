from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pepperpy.core.logging import get_logger

from ..exceptions import ModelNotFoundError
from ..types import AIResponse, Message


class BaseProvider(ABC):
    """Base class for AI providers"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._initialized = False
        self._logger = get_logger(f"ai.providers.{self.__class__.__name__.lower()}")

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize provider"""
        pass

    @abstractmethod
    async def list_models(self) -> List[str]:
        """List available models"""
        pass

    @abstractmethod
    async def generate(self, messages: List[Message], **kwargs) -> AIResponse:
        """Generate response from prompt"""
        pass

    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        self._initialized = False

    def _validate_model(self, model: Optional[str] = None) -> str:
        """Validate model availability"""
        if not model and "model" not in self.config:
            raise ModelNotFoundError("No model specified")
        return model or self.config["model"]

    @property
    def initialized(self) -> bool:
        """Check if provider is initialized"""
        return self._initialized
