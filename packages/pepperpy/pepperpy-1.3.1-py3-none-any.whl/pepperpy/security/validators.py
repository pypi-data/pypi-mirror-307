"""Security validation utilities"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PasswordValidator:
    """Password validation rules"""

    min_length: int = 8
    require_special: bool = True
    require_numbers: bool = True
    special_chars: str = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    max_length: Optional[int] = None
    require_uppercase: bool = True
    require_lowercase: bool = True
    forbidden_words: List[str] = None

    def __post_init__(self):
        self.forbidden_words = self.forbidden_words or []

    def validate(self, password: str) -> bool:
        """Validate password against rules"""
        if len(password) < self.min_length:
            return False

        if self.max_length and len(password) > self.max_length:
            return False

        if self.require_numbers and not any(c.isdigit() for c in password):
            return False

        if self.require_special and not any(c in self.special_chars for c in password):
            return False

        if self.require_uppercase and not any(c.isupper() for c in password):
            return False

        if self.require_lowercase and not any(c.islower() for c in password):
            return False

        if any(word.lower() in password.lower() for word in self.forbidden_words):
            return False

        return True

    def get_requirements(self) -> List[str]:
        """Get list of password requirements"""
        reqs = [f"Minimum length: {self.min_length} characters"]

        if self.max_length:
            reqs.append(f"Maximum length: {self.max_length} characters")
        if self.require_numbers:
            reqs.append("Must contain at least one number")
        if self.require_special:
            reqs.append(f"Must contain at least one special character ({self.special_chars})")
        if self.require_uppercase:
            reqs.append("Must contain at least one uppercase letter")
        if self.require_lowercase:
            reqs.append("Must contain at least one lowercase letter")
        if self.forbidden_words:
            reqs.append("Must not contain forbidden words")

        return reqs
