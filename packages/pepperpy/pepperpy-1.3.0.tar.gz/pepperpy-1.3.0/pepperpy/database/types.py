from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field


class PoolConfig(BaseModel):
    """Database connection pool configuration"""

    size: int = Field(default=5, ge=1)
    max_overflow: int = Field(default=10, ge=0)
    timeout: int = Field(default=30, ge=0)
    recycle: int = Field(default=1800, ge=0)


class SSLConfig(BaseModel):
    """SSL configuration"""

    enabled: bool = False
    verify: bool = True
    ca_cert: Optional[str] = None
    client_cert: Optional[str] = None
    client_key: Optional[str] = None


class ConnectionConfig(BaseModel):
    """Database connection configuration"""

    url: str
    options: Dict[str, Any] = Field(default_factory=dict)
    ssl: Union[bool, SSLConfig] = False
    timeout: int = Field(default=60, ge=0)
    application_name: Optional[str] = None


class RetryConfig(BaseModel):
    """Retry configuration"""

    enabled: bool = True
    max_attempts: int = Field(default=3, ge=1)
    delay: float = Field(default=1.0, ge=0)
    backoff: float = Field(default=2.0, ge=1)


class DatabaseConfig(BaseModel):
    """Database module configuration"""

    backend: str = "postgresql"
    connection: ConnectionConfig
    pool: PoolConfig = Field(default_factory=PoolConfig)
    retry: RetryConfig = Field(default_factory=RetryConfig)
    debug: bool = False
    auto_migrate: bool = True
    autoflush: bool = True
    timezone: str = "UTC"
