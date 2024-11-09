"""Configuration management system"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .exceptions import ConfigurationError
from .types import Validator


@dataclass
class ConfigSource:
    """Configuration source definition"""

    location: str
    required: bool = False
    format: str = "yaml"


@dataclass
class Config:
    """Base configuration class"""

    default_config: Dict[str, Any] = field(default_factory=dict)
    env_prefix: str = "PEPPERPY"
    config_sources: List[ConfigSource] = field(default_factory=list)
    validator: Optional[Validator] = None

    def load(self) -> None:
        """Load configuration from all sources"""
        config = self.default_config.copy()

        # Load from files
        for source in self.config_sources:
            try:
                source_config = self._load_source(source)
                config.update(source_config)
            except Exception as e:
                if source.required:
                    raise ConfigurationError(
                        f"Failed to load required config from {source.location}: {e}"
                    ) from e

        # Load from environment
        env_config = self._load_environment()
        config.update(env_config)

        # Validate configuration
        if self.validator:
            self.validator.validate(config)

        self._config = config

    def _load_source(self, source: ConfigSource) -> Dict[str, Any]:
        """Load configuration from source"""
        # Implementação do carregamento de fonte
        pass

    def _load_environment(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        # Implementação do carregamento de variáveis de ambiente
        pass
