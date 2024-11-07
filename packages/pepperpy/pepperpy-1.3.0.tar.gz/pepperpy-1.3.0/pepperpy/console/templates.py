from string import Template
from typing import ClassVar, Dict


class ConsoleTemplates:
    """Templates para mensagens comuns"""

    _templates: ClassVar[Dict[str, str]] = {
        "welcome": "Welcome to $app_name v$version",
        "goodbye": "Thanks for using $app_name",
        "loading": "Loading $resource...",
        "saving": "Saving $resource...",
        "error": "Error: $message",
        "success": "Success: $message",
        "confirm": "Are you sure you want to $action?",
        "input": "Please enter $field",
        "invalid": "Invalid $field: $message",
        "not_found": "$resource not found",
        "processing": "Processing $item... ($current/$total)",
    }

    @classmethod
    def get(cls, key: str, **kwargs: str) -> str:
        """Get formatted template"""
        template = cls._templates.get(key)
        if not template:
            raise KeyError(f"Template '{key}' not found")
        return Template(template).safe_substitute(**kwargs)

    @classmethod
    def add(cls, key: str, template: str) -> None:
        """Add custom template"""
        cls._templates[key] = template
