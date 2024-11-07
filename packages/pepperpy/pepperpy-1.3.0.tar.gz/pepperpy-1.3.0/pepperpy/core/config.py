import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

import yaml

from .exceptions import ConfigError
from .types import JsonDict, PathLike


class ConfigProvider(ABC):
    """Interface para provedores de configuração"""

    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Obtém valor de configuração"""
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Define valor de configuração"""
        pass


class FileConfigProvider(ConfigProvider):
    """Provedor de configuração baseado em arquivo"""

    def __init__(self, path: PathLike):
        self.path = Path(path)
        self._config = self._load()

    def _load(self) -> JsonDict:
        """Carrega configuração do arquivo"""
        try:
            if not self.path.exists():
                return {}

            if self.path.suffix == ".json":
                with open(self.path) as f:
                    return json.load(f)
            elif self.path.suffix in (".yml", ".yaml"):
                with open(self.path) as f:
                    return yaml.safe_load(f)
            else:
                raise ConfigError(f"Unsupported config format: {self.path.suffix}")
        except Exception as e:
            raise ConfigError(f"Error loading config: {str(e)}") from e

    def get(self, key: str, default: Any = None) -> Any:
        """Obtém valor de configuração"""
        try:
            value = self._config
            for part in key.split("."):
                value = value.get(part, {})
            return value or default
        except Exception as e:
            raise ConfigError(f"Error getting config value: {str(e)}") from e

    def set(self, key: str, value: Any) -> None:
        """Define valor de configuração"""
        try:
            parts = key.split(".")
            config = self._config
            for part in parts[:-1]:
                config = config.setdefault(part, {})
            config[parts[-1]] = value

            with open(self.path, "w") as f:
                if self.path.suffix == ".json":
                    json.dump(self._config, f, indent=2)
                else:
                    yaml.dump(self._config, f)
        except Exception as e:
            raise ConfigError(f"Error setting config value: {str(e)}") from e


class Config:
    """Gerenciador de configuração"""

    def __init__(self, provider: Optional[ConfigProvider] = None):
        self.provider = provider or FileConfigProvider("config.yml")

    def get(self, key: str, default: Any = None) -> Any:
        return self.provider.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.provider.set(key, value)
