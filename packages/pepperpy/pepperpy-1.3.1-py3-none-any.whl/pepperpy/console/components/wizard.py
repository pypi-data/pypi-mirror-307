"""Configuration wizard component"""

import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Pattern, Union

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt


@dataclass
class WizardStep:
    """Configuration wizard step"""

    name: str
    prompt: str
    value_type: type = str
    choices: Optional[List[str]] = None
    default: Any = None
    required: bool = True
    multiple: bool = False
    pattern: Optional[Union[str, Pattern]] = None
    validator: Optional[Callable[[Any], bool]] = None
    help_text: Optional[str] = None


class ConfigWizard:
    """Interactive configuration wizard"""

    def __init__(self, console: Console):
        self._console = console

    async def run(self, title: str, steps: List[WizardStep]) -> Dict[str, Any]:
        """Run configuration wizard.

        Args:
            title: Wizard title
            steps: Configuration steps

        Returns:
            Dict[str, Any]: Collected configuration
        """
        self._console.print(Panel(f"[bold blue]{title}[/]"))

        config = {}
        for step in steps:
            value = await self._get_input(step)
            if value is not None:
                config[step.name] = value

        return config

    async def _get_input(self, step: WizardStep) -> Any:
        """Get user input for a wizard step."""
        while True:
            try:
                # Show help text if available
                if step.help_text:
                    self._console.print(f"[dim]{step.help_text}[/]")

                # Handle multiple selection
                if step.multiple and step.choices:
                    return self._handle_multiple_choice(step)

                # Handle single input
                value = Prompt.ask(step.prompt, choices=step.choices, default=step.default)

                # Handle empty input
                if not value:
                    if step.required:
                        self._console.print("[red]This field is required[/]")
                        continue
                    return step.default

                # Validate pattern
                if step.pattern:
                    pattern = (
                        step.pattern
                        if isinstance(step.pattern, Pattern)
                        else re.compile(step.pattern)
                    )
                    if not pattern.match(value):
                        self._console.print("[red]Invalid format[/]")
                        continue

                # Convert type
                value = step.value_type(value)

                # Custom validation
                if step.validator and not step.validator(value):
                    self._console.print("[red]Validation failed[/]")
                    continue

                return value

            except ValueError:
                self._console.print(
                    f"[red]Invalid input. Expected type: {step.value_type.__name__}[/]"
                )

    def _handle_multiple_choice(self, step: WizardStep) -> List[str]:
        """Handle multiple choice selection."""
        selected = step.default or []
        while True:
            self._console.print("\nCurrent selection:", ", ".join(selected))
            value = Prompt.ask(f"{step.prompt} (empty to finish)", choices=step.choices, default="")

            if not value:
                if not selected and step.required:
                    self._console.print("[red]At least one selection is required[/]")
                    continue
                return selected

            if value not in selected:
                selected.append(value)
