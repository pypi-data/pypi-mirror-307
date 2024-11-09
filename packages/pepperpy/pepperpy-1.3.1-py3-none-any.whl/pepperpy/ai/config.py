import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from .exceptions import ConfigurationError


@dataclass
class AIConfig:
    """Configuration for AI module"""

    provider: str
    model: Optional[str] = None
    api_key: Optional[str] = None
    client_id: Optional[str] = None
    client_key: Optional[str] = None
    realm: Optional[str] = None
    max_retries: int = 3
    timeout: float = 30.0
    debug: bool = False

    @classmethod
    def from_env(cls) -> "AIConfig":
        """Create configuration from environment variables"""
        load_dotenv()

        provider = os.getenv("AI_PROVIDER", "openrouter").lower()
        config_dict = {"provider": provider}

        if provider == "openrouter":
            config_dict.update(
                {
                    "api_key": os.getenv("OPENROUTER_API_KEY"),
                    "model": os.getenv("OPENROUTER_MODEL", "openai/gpt-4-turbo-preview"),
                }
            )
        elif provider == "stackspot":
            config_dict.update(
                {
                    "client_id": os.getenv("STACKSPOT_CLIENT_ID"),
                    "client_key": os.getenv("STACKSPOT_CLIENT_KEY"),
                    "realm": os.getenv("STACKSPOT_REALM"),
                }
            )

        try:
            return cls(**config_dict)
        except TypeError as e:
            raise ConfigurationError(f"Invalid configuration: {str(e)}") from e

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {k: v for k, v in self.__dict__.items() if v is not None}
