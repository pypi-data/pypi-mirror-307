from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

import yaml
from jinja2 import BaseLoader, Environment


@dataclass
class PromptTemplate:
    """Template for AI prompts"""

    name: str
    template: str
    description: Optional[str] = None
    variables: List[str] = field(default_factory=list)
    examples: List[Dict[str, Any]] = field(default_factory=list)

    def render(self, **kwargs: Union[str, int, float, bool, list, dict]) -> str:
        """Render template with variables"""
        env = Environment(loader=BaseLoader())
        template = env.from_string(self.template)
        return template.render(**kwargs)

    def validate_variables(self, variables: Dict[str, Any]) -> List[str]:
        """Validate required variables"""
        missing = []
        for var in self.variables:
            if var not in variables:
                missing.append(var)
        return missing


class PromptManager:
    """Manages prompt templates and generation"""

    def __init__(self) -> None:
        self._templates: Dict[str, PromptTemplate] = {}

    def load_templates(self, path: str) -> None:
        """Load templates from YAML file"""
        with open(path) as f:
            data = yaml.safe_load(f)

        for name, config in data.get("templates", {}).items():
            self._templates[name] = PromptTemplate(
                name=name,
                template=config["template"],
                description=config.get("description"),
                variables=config.get("variables", []),
                examples=config.get("examples", []),
            )

    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Get template by name"""
        return self._templates.get(name)

    def render_template(self, name: str, variables: Dict[str, Any]) -> Optional[str]:
        """Render template with variables"""
        template = self.get_template(name)
        if not template:
            return None

        # Validate variables
        missing = template.validate_variables(variables)
        if missing:
            raise ValueError(f"Missing variables: {', '.join(missing)}")

        return template.render(**variables)

    def export_templates(self, path: str) -> None:
        """Export templates to file"""
        data = {
            "templates": {
                name: {
                    "template": template.template,
                    "description": template.description,
                    "variables": template.variables,
                    "examples": template.examples,
                }
                for name, template in self._templates.items()
            }
        }

        with open(path, "w") as f:
            yaml.dump(data, f, sort_keys=False)
