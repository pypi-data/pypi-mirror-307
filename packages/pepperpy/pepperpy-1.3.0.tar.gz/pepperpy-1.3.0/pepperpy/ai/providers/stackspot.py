from typing import Any, Dict, List, Optional

import aiohttp

from ..module import AIResponse, BaseProvider, ModelNotFoundError


class StackSpotProvider(BaseProvider):
    """StackSpot AI provider implementation"""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.api_key = config["api_key"]
        self.base_url = "https://api.stackspot.ai/v1"
        self.workspace_id = config.get("workspace_id")

    async def generate(self, prompt: str, model: Optional[str] = None, **kwargs) -> AIResponse:
        """Generate response using StackSpot AI"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        if self.workspace_id:
            headers["X-Workspace-ID"] = self.workspace_id

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json={"messages": [{"role": "user", "content": prompt}], **kwargs},
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise ModelNotFoundError(
                        f"StackSpot error: {data.get('error', {}).get('message')}"
                    )

                return AIResponse(
                    content=data["choices"][0]["message"]["content"],
                    model=data.get("model", "stackspot-default"),
                    usage=data.get("usage", {}),
                    metadata={
                        "provider": "stackspot",
                        "workspace_id": self.workspace_id,
                    },
                )

    async def list_models(self) -> List[str]:
        """List available StackSpot models"""
        # StackSpot AI currently uses a single model
        return ["stackspot-default"]
