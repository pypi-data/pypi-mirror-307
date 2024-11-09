"""Encryption utilities"""

import base64
from typing import Union

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class AESEncryption:
    """AES encryption wrapper"""

    def __init__(self, key: str):
        """Initialize encryption with key"""
        self._fernet = self._create_fernet(key)

    def encrypt(self, data: Union[str, bytes]) -> str:
        """Encrypt data"""
        if isinstance(data, str):
            data = data.encode()
        encrypted = self._fernet.encrypt(data)
        return base64.urlsafe_b64encode(encrypted).decode()

    def decrypt(self, encrypted: str) -> Union[str, bytes]:
        """Decrypt data"""
        try:
            data = base64.urlsafe_b64decode(encrypted.encode())
            decrypted = self._fernet.decrypt(data)
            try:
                return decrypted.decode()
            except UnicodeDecodeError:
                return decrypted
        except Exception as e:
            raise ValueError(f"Failed to decrypt data: {e}") from e

    def _create_fernet(self, key: str) -> Fernet:
        """Create Fernet instance from key"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"pepperpy",  # Fixed salt for reproducibility
            iterations=100000,
        )
        key_bytes = key.encode()
        key = base64.urlsafe_b64encode(kdf.derive(key_bytes))
        return Fernet(key)
