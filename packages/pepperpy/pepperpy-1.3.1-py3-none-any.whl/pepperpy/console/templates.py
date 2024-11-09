from string import Template
from typing import Any, Dict


class ConsoleTemplates:
    """Console message template manager"""

    _templates: Dict[str, str] = {}

    @classmethod
    def add(cls, name: str, template: str) -> None:
        """Add a new template.

        Args:
            name: Template identifier
            template: Template string with $variable placeholders
        """
        cls._templates[name] = template

    @classmethod
    def get(cls, name: str, **kwargs: Any) -> str:
        """Get rendered template with variables.

        Args:
            name: Template identifier
            **kwargs: Template variables

        Returns:
            Rendered template string

        Raises:
            KeyError: If template not found
        """
        template = cls._templates.get(name)
        if template is None:
            raise KeyError(
                f"Template '{name}' not found. Available templates: {list(cls._templates.keys())}"
            )

        return Template(template).safe_substitute(**kwargs)

    @classmethod
    def clear(cls) -> None:
        """Remove all templates."""
        cls._templates.clear()
