import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

import bcrypt
import jwt

from pepperpy.core import BaseModule, ModuleConfig

from .encryption import AESEncryption
from .validators import PasswordValidator


@dataclass
class SecurityConfig(ModuleConfig):
    secret_key: str
    token_expiration: int = 3600  # 1 hour
    password_min_length: int = 8
    password_require_special: bool = True
    password_require_numbers: bool = True
    encryption_key_size: int = 32
    hash_rounds: int = 12


class SecurityModule(BaseModule):
    """Security utilities for authentication and encryption"""

    __module_name__ = "security"
    __dependencies__ = ["cache"]

    def __init__(self, config: Optional[SecurityConfig] = None):
        super().__init__(config or SecurityConfig())
        self._encryption = None
        self._password_validator = None

    async def initialize(self) -> None:
        await super().initialize()
        self._encryption = AESEncryption(self.config.secret_key)
        self._password_validator = PasswordValidator(
            min_length=self.config.password_min_length,
            require_special=self.config.password_require_special,
            require_numbers=self.config.password_require_numbers,
        )

    def create_token(self, data: Dict[str, Any], expires_in: Optional[int] = None) -> str:
        """Create JWT token"""
        payload = data.copy()
        exp = datetime.utcnow() + timedelta(seconds=expires_in or self.config.token_expiration)
        payload["exp"] = exp.timestamp()

        return jwt.encode(payload, self.config.secret_key, algorithm="HS256")

    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            return jwt.decode(token, self.config.secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError as e:
            raise ValueError("Token expired") from e
        except jwt.InvalidTokenError as e:
            raise ValueError("Invalid token") from e

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        if not self._password_validator.validate(password):
            raise ValueError("Password does not meet requirements")

        salt = bcrypt.gensalt(rounds=self.config.hash_rounds)
        return bcrypt.hashpw(password.encode(), salt).decode()

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode(), hashed.encode())

    def encrypt(self, data: Union[str, bytes]) -> str:
        """Encrypt data using AES"""
        return self._encryption.encrypt(data)

    def decrypt(self, encrypted: str) -> Union[str, bytes]:
        """Decrypt AES encrypted data"""
        return self._encryption.decrypt(encrypted)

    def generate_key(self, size: Optional[int] = None) -> str:
        """Generate secure random key"""
        return secrets.token_urlsafe(size or self.config.encryption_key_size)
