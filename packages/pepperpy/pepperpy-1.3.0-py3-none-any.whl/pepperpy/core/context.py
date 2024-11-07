from typing import Any, Dict


class Context:
    """Module context for sharing data"""

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from context"""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set value in context"""
        self._data[key] = value
