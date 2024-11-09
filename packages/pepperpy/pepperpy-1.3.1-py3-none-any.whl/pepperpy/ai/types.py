from dataclasses import asdict, dataclass
from typing import Any, Dict, Literal, Optional


@dataclass
class Message:
    """Chat message"""

    role: Literal["system", "user", "assistant"]
    content: str
    name: Optional[str] = None

    def to_dict(self) -> Dict[str, str]:
        """Convert message to dictionary"""
        # Remove None values and convert to dict
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class AIResponse:
    """Response from AI provider"""

    content: str
    model: str
    provider: str
    raw_response: Optional[Dict[str, Any]] = None
    usage: Optional[Dict[str, int]] = None
