"""Core settings and configuration management"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Union

import tomli
import yaml
from dotenv import load_dotenv


@dataclass
class Settings:
    """Global settings container with environment support"""

    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        self._config: Dict[str, Any] = {}
        self._env_prefix = "PEPPERPY_"

        # Load .env file if exists
        load_dotenv()

        # Load config file if provided
        if config_path:
            self.load_config(config_path)

        # Load environment variables
        self._load_env_vars()

    def load_config(self, path: Union[str, Path]) -> None:
        """Load configuration from file"""
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with open(path, "rb") as f:
            if path.suffix in (".toml", ".tml"):
                self._config.update(tomli.load(f))
            elif path.suffix in (".yaml", ".yml"):
                self._config.update(yaml.safe_load(f))
            else:
                raise ValueError(f"Unsupported config format: {path.suffix}")

    def _load_env_vars(self) -> None:
        """Load environment variables with prefix"""
        for key, value in os.environ.items():
            if key.startswith(self._env_prefix):
                config_key = key[len(self._env_prefix) :].lower()
                self._config[config_key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._config.get(key, default)

    def __getattr__(self, key: str) -> Any:
        """Allow attribute-style access"""
        return self.get(key)
