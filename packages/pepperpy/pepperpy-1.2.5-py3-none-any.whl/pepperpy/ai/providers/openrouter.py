from typing import Any, Dict, List, Optional

import aiohttp

from ..module import AIResponse, BaseProvider, ModelNotFoundError


class OpenRouterProvider(BaseProvider):
    """OpenRouter AI provider implementation"""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.api_key = config["api_key"]
        self.base_url = "https://openrouter.ai/api/v1"
        self.default_model = config.get("default_model", "openai/gpt-3.5-turbo")

    async def generate(self, prompt: str, model: Optional[str] = None, **kwargs) -> AIResponse:
        """Generate response using OpenRouter"""
        model = model or self.default_model

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    **kwargs,
                },
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise ModelNotFoundError(
                        f"OpenRouter error: {data.get('error', {}).get('message')}"
                    )

                return AIResponse(
                    content=data["choices"][0]["message"]["content"],
                    model=data["model"],
                    usage=data.get("usage", {}),
                    metadata={"provider": "openrouter"},
                )

    async def list_models(self) -> List[str]:
        """List available OpenRouter models"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
            ) as response:
                data = await response.json()
                return [model["id"] for model in data]
