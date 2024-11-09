from typing import Any, Dict, List

import httpx

from ..exceptions import ProviderError
from ..types import AIResponse, Message
from .base import BaseProvider


class OpenRouterProvider(BaseProvider):
    """OpenRouter API provider implementation"""

    API_BASE = "https://openrouter.ai/api/v1"

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._api_key = config.get("api_key")
        if not self._api_key:
            raise ProviderError("OpenRouter API key not provided")

    async def initialize(self) -> None:
        """Initialize OpenRouter provider"""
        self._initialized = True
        self._logger.info(f"OpenRouter provider initialized with model: {self.config.get('model')}")

    async def list_models(self) -> List[str]:
        """List available OpenRouter models"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.API_BASE}/models",
                headers=self._get_headers(),
            )
            response.raise_for_status()
            data = response.json()
            return [model["id"] for model in data.get("data", [])]

    async def generate(self, messages: List[Message], **kwargs) -> AIResponse:
        """Generate response using OpenRouter"""
        model = self._validate_model()
        self._logger.debug(f"Generating response using model: {model}")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.API_BASE}/chat/completions",
                    headers=self._get_headers(),
                    json={
                        "model": model,
                        "messages": [msg.to_dict() for msg in messages],
                        **kwargs,
                    },
                )
                response.raise_for_status()
                data = response.json()

                return AIResponse(
                    content=data["choices"][0]["message"]["content"],
                    model=model,
                    provider="openrouter",
                    raw_response=data,
                    usage=data.get("usage"),
                )
        except httpx.HTTPStatusError as e:
            self._logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise ProviderError(f"OpenRouter request failed: {e.response.text}") from e
        except Exception as e:
            self._logger.error(f"Error generating response: {str(e)}")
            raise ProviderError(f"Failed to generate response: {str(e)}") from e

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        return {
            "Authorization": f"Bearer {self._api_key}",
            "HTTP-Referer": "https://github.com/pepperpydev/pepperpy",
            "X-Title": "PepperPy AI Module",
        }
