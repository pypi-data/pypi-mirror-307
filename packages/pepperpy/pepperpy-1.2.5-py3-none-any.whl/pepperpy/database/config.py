from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, field_validator

from pepperpy.core.config import ConfigProvider

from .types import ConnectionConfig, PoolConfig, RetryConfig


class DatabaseModuleConfig(BaseModel):
    """Database module configuration with validation"""

    enabled: bool = True
    debug: bool = False
    backend: str = Field(default="postgresql")
    connection: ConnectionConfig
    pool: Optional[PoolConfig] = Field(default_factory=PoolConfig)
    retry: Optional[RetryConfig] = Field(default_factory=RetryConfig)
    auto_migrate: bool = True
    migrations_dir: str = "migrations"

    @field_validator("backend")
    @classmethod
    def validate_backend(cls, v: str) -> str:
        valid_backends = ["postgresql", "mysql", "sqlite", "duckdb"]
        if v not in valid_backends:
            raise ValueError(f"Backend must be one of: {', '.join(valid_backends)}")
        return v

    class Config:
        extra = "forbid"


class DatabaseConfigProvider(ConfigProvider):
    """Configuration provider for database module"""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = DatabaseModuleConfig(**config)

    def get(
        self, key: str, default: str | int | bool | dict | None = None
    ) -> str | int | bool | dict | None:
        """Get configuration value"""
        try:
            parts = key.split(".")
            value = self.config
            for part in parts:
                value = getattr(value, part)
            return value
        except AttributeError:
            return default

    def set(self, key: str, value: str | int | bool | dict) -> None:
        """Set configuration value"""
        parts = key.split(".")
        target = self.config
        for part in parts[:-1]:
            target = getattr(target, part)
        setattr(target, parts[-1], value)
