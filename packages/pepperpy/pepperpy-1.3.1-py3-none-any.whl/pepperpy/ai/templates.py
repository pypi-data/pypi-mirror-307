from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import yaml
from jinja2 import BaseLoader, Environment


@dataclass
class PromptTemplate:
    """Template for AI prompts"""

    name: str
    template: str
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def render(self, **kwargs: str | int | float | bool) -> str:
        """Render template with variables"""
        env = Environment(loader=BaseLoader())
        template = env.from_string(self.template)
        return template.render(**kwargs)


class TemplateManager:
    """Manages prompt templates"""

    def __init__(self) -> None:
        self._templates: Dict[str, PromptTemplate] = {}

    def load_from_file(self, path: str) -> None:
        """Load templates from YAML file"""
        with open(path) as f:
            data = yaml.safe_load(f)
            for name, config in data.get("templates", {}).items():
                self._templates[name] = PromptTemplate(
                    name=name,
                    template=config["template"],
                    description=config.get("description"),
                    metadata=config.get("metadata", {}),
                )

    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Get template by name"""
        return self._templates.get(name)

    def render_template(self, name: str, **kwargs: str | int | float | bool) -> Optional[str]:
        """Render template with variables"""
        template = self.get_template(name)
        if template:
            return template.render(**kwargs)
        return None
