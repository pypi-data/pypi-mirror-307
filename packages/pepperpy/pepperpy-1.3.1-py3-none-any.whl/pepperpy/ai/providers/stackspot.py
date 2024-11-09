from typing import Any, Dict, List
from urllib.parse import urljoin

import httpx

from ..exceptions import ProviderError
from ..types import AIResponse, Message
from .base import BaseProvider


class StackSpotProvider(BaseProvider):
    """StackSpot AI provider implementation"""

    API_BASE = "https://api.stackspot.com/v1"  # Ajustado para incluir versão
    DEFAULT_MODEL = "gpt-4"

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._client_id = config.get("client_id")
        self._client_key = config.get("client_key")
        self._realm = config.get("realm")
        self._model = config.get("model", self.DEFAULT_MODEL)

        # Validação mais detalhada das credenciais
        missing = []
        if not self._client_id:
            missing.append("STACKSPOT_CLIENT_ID")
        if not self._client_key:
            missing.append("STACKSPOT_CLIENT_KEY")
        if not self._realm:
            missing.append("STACKSPOT_REALM")

        if missing:
            raise ProviderError(
                f"Missing StackSpot credentials: {', '.join(missing)}. "
                "Please set these environment variables or provide them in the configuration."
            )

    async def initialize(self) -> None:
        """Initialize StackSpot provider"""
        try:
            # Validar credenciais fazendo uma chamada de teste
            self._logger.debug("Validating StackSpot credentials...")
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    urljoin(self.API_BASE, "auth/validate"),
                    headers=self._get_headers(),
                    timeout=10.0,
                )

                if response.status_code == 401:
                    raise ProviderError("Invalid StackSpot credentials")
                elif response.status_code == 403:
                    raise ProviderError(
                        "Access forbidden. Please check your StackSpot credentials and permissions"
                    )

                response.raise_for_status()

            self._initialized = True
            self._logger.info(f"StackSpot provider initialized with model: {self._model}")

        except httpx.HTTPStatusError as e:
            raise ProviderError(
                f"HTTP error during initialization: {e.response.status_code} - {e.response.text}"
            ) from e
        except httpx.RequestError as e:
            raise ProviderError(f"Request error during initialization: {str(e)}") from e
        except Exception as e:
            raise ProviderError(f"Failed to initialize StackSpot provider: {str(e)}") from e

    async def list_models(self) -> List[str]:
        """List available StackSpot models"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    urljoin(self.API_BASE, "models"), headers=self._get_headers(), timeout=10.0
                )

                if response.status_code == 401:
                    raise ProviderError("Invalid StackSpot credentials")
                elif response.status_code == 403:
                    raise ProviderError("Access forbidden. Please check your permissions")

                response.raise_for_status()
                data = response.json()
                return [model["id"] for model in data.get("models", [])]

        except httpx.HTTPStatusError as e:
            raise ProviderError(
                f"Failed to list models: {e.response.status_code} - {e.response.text}"
            ) from e
        except Exception as e:
            raise ProviderError(f"Failed to list StackSpot models: {str(e)}") from e

    async def generate(self, messages: List[Message], **kwargs) -> AIResponse:
        """Generate response using StackSpot"""
        try:
            model = kwargs.pop("model", None) or self._model
            self._logger.debug(f"Generating response using model: {model}")

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    urljoin(self.API_BASE, "chat/completions"),
                    headers=self._get_headers(),
                    json={
                        "messages": [
                            {"role": msg.role, "content": msg.content} for msg in messages
                        ],
                        "model": model,
                        **kwargs,
                    },
                    timeout=30.0,
                )

                if response.status_code == 401:
                    raise ProviderError("Invalid StackSpot credentials")
                elif response.status_code == 403:
                    raise ProviderError("Access forbidden. Please check your permissions")

                response.raise_for_status()
                data = response.json()

                return AIResponse(
                    content=data["choices"][0]["message"]["content"],
                    model=model,
                    provider="stackspot",
                    raw_response=data,
                    usage=data.get("usage"),
                )

        except httpx.HTTPStatusError as e:
            self._logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise ProviderError(
                f"Failed to generate response: {e.response.status_code} - {e.response.text}"
            ) from e
        except httpx.RequestError as e:
            self._logger.error(f"Request error: {str(e)}")
            raise ProviderError(f"Request failed: {str(e)}") from e
        except Exception as e:
            self._logger.error(f"Unexpected error: {str(e)}")
            raise ProviderError(f"Failed to generate response: {str(e)}") from e

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        return {
            "X-Client-ID": self._client_id,
            "X-Client-Key": self._client_key,
            "X-Realm": self._realm,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "PepperPy/1.0",
        }
