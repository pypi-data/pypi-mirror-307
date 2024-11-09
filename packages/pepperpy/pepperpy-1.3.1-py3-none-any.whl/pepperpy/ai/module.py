from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict, Optional, Type, Union

from pepperpy.core.base import BaseModule, ModuleStatus
from pepperpy.core.logging import get_logger

from .config import AIConfig
from .exceptions import AIError, InitializationError, ProviderError
from .providers.base import BaseProvider
from .types import AIResponse, Message


class AIModule(BaseModule):
    """AI module implementation"""

    __module_name__ = "ai"

    def __init__(self, config: Optional[Union[Dict[str, Any], AIConfig]] = None):
        """Initialize AI module with optional config"""
        if isinstance(config, dict):
            config = AIConfig(**config)
        elif config is None:
            config = AIConfig.from_env()

        super().__init__(config.to_dict())
        self._provider: Optional[BaseProvider] = None
        self._config = config
        self._logger = get_logger("ai.module")

    @classmethod
    @asynccontextmanager
    async def session(
        cls, config: Optional[Union[Dict[str, Any], AIConfig]] = None
    ) -> AsyncIterator["AIModule"]:
        """Create a managed AI session"""
        module = cls(config)
        try:
            await module.setup()
            yield module
        finally:
            await module.cleanup()

    @classmethod
    async def create(cls, config: Optional[Union[Dict[str, Any], AIConfig]] = None) -> "AIModule":
        """Create and initialize AI module"""
        module = cls(config)
        await module.setup()
        return module

    async def setup(self) -> None:
        """Setup module - required by BaseModule"""
        try:
            await self.initialize()
            self._status = ModuleStatus.ACTIVE
        except Exception as e:
            self._logger.error(f"Setup failed: {str(e)}")
            self._status = ModuleStatus.ERROR
            raise InitializationError(str(e)) from e

    async def initialize(self) -> None:
        """Initialize AI module"""
        provider_class = self._get_provider_class(self._config.provider)
        try:
            self._provider = provider_class(self._config.to_dict())
            await self._provider.initialize()
        except Exception as e:
            raise ProviderError(f"Provider initialization failed: {str(e)}") from e

    async def ask(self, prompt: str, **kwargs) -> str:
        """Simple method to get AI response as string"""
        try:
            response = await self.generate(prompt, **kwargs)
            return response.content
        except Exception as e:
            self._logger.error(f"Error in ask: {str(e)}")
            raise ProviderError(f"Failed to generate response: {str(e)}") from e

    async def generate(self, prompt: Union[str, Message, list[Message]], **kwargs) -> AIResponse:
        """Generate AI response with full context"""
        if not self._provider:
            raise ProviderError("Provider not initialized")

        try:
            # Convert prompt to proper format
            if isinstance(prompt, str):
                messages = [Message(role="user", content=prompt)]
            elif isinstance(prompt, Message):
                messages = [prompt]
            else:
                messages = prompt

            return await self._provider.generate(messages, **kwargs)
        except Exception as e:
            self._logger.error(f"Error in generate: {str(e)}")
            raise ProviderError(f"Failed to generate response: {str(e)}") from e

    def _get_provider_class(self, provider_name: str) -> Type[BaseProvider]:
        """Get provider class by name"""
        if provider_name == "stackspot":
            from .providers.stackspot import StackSpotProvider

            return StackSpotProvider
        elif provider_name == "openrouter":
            from .providers.openrouter import OpenRouterProvider

            return OpenRouterProvider
        else:
            raise AIError(f"Unknown provider: {provider_name}")

    async def cleanup(self) -> None:
        """Cleanup AI module"""
        try:
            if self._provider:
                await self._provider.cleanup()
            self._status = ModuleStatus.INACTIVE
        except Exception as e:
            self._logger.error(f"Error in cleanup: {str(e)}")
            self._status = ModuleStatus.ERROR
            raise
