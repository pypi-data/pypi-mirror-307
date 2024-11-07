import json
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Union

import yaml
from rich.console import Console as RichConsole
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.theme import Theme

from .exceptions import ConsoleDisplayError, ConsoleInputError
from .types import ConsoleConfig, Style

JSONValue = Union[Dict[str, "JSONValue"], List["JSONValue"], str, int, float, bool, None]


class Console:
    """
    Console simplificado para desenvolvimento rápido
    """

    def __init__(self, config: Optional[ConsoleConfig] = None) -> None:
        self.theme = Theme(
            {
                Style.INFO: "cyan",
                Style.WARNING: "yellow",
                Style.ERROR: "red",
                Style.SUCCESS: "green",
                Style.HIGHLIGHT: "magenta",
                Style.MUTED: "dim white",
                Style.CODE: "blue",
                Style.DATA: "green",
                Style.URL: "underline cyan",
            }
        )

        self.console = RichConsole(theme=self.theme)

    def clear(self) -> None:
        """Clear the console screen"""
        self.console.clear()

    def print(self, message: str, style: Optional[Style] = None) -> None:
        """Print message with optional style"""
        try:
            self.console.print(message, style=style)
        except Exception as e:
            raise ConsoleDisplayError(f"Error printing message: {e!s}") from e

    def title(self, text: str) -> None:
        """Display a title"""
        self.console.print(f"\n[bold]{text}[/bold]\n")

    def divider(self) -> None:
        """Display a divider line"""
        self.console.print("─" * 40)

    # Logging methods
    def log(self, message: str, style: Optional[str] = None) -> None:
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.print(f"[muted]{timestamp}[/muted] {message}", style=style)

    def info(self, message: str) -> None:
        """Log info message"""
        self.log(f"[i] {message}", style=Style.INFO)

    def success(self, message: str) -> None:
        """Log success message"""
        self.log(f"✓ {message}", style=Style.SUCCESS)

    def warning(self, message: str) -> None:
        """Log warning message"""
        self.log(f"⚠ {message}", style=Style.WARNING)

    def error(self, message: str) -> None:
        """Log error message"""
        self.log(f"✗ {message}", style=Style.ERROR)

    # Input methods
    def ask(
        self,
        message: str,
        choices: Optional[List[str]] = None,
        default: Optional[str] = None,
        password: bool = False,
    ) -> str:
        """Get user input with optional choices"""
        try:
            return Prompt.ask(
                message,
                choices=choices,
                default=default,
                password=password,
                console=self.console,
            )
        except KeyboardInterrupt as err:
            raise ConsoleInputError("Input cancelled by user") from err

    def confirm(self, message: str, default: bool = True) -> bool:
        """Get yes/no confirmation from user"""
        try:
            return Confirm.ask(message, default=default, console=self.console)
        except KeyboardInterrupt as err:
            raise ConsoleInputError("Input cancelled by user") from err

    # Data display methods
    def table(
        self,
        data: List[Dict[str, Any]],
        columns: Optional[List[str]] = None,
        title: Optional[str] = None,
    ) -> None:
        """Display data in table format"""
        try:
            table = Table(title=title)

            # Auto-detect columns if not provided
            if not columns and data:
                columns = list(data[0].keys())

            for col in columns:
                table.add_column(col)

            for row in data:
                table.add_row(*[str(row.get(col, "")) for col in columns])

            self.console.print(table)
        except Exception as e:
            raise ConsoleDisplayError(f"Error creating table: {e!s}") from e

    def show(
        self,
        data: Union[Dict[str, Any], List[Any], str, int, float, bool, None],
        title: Optional[str] = None,
    ) -> None:
        """Display data in appropriate format"""
        if isinstance(data, (dict, list)):
            self.show_json(data, title)
        else:
            self.console.print(str(data))

    def show_json(self, data: Union[str, Dict], title: Optional[str] = None) -> None:
        """Display formatted JSON"""
        try:
            if isinstance(data, str):
                data = json.loads(data)
            if title:
                self.title(title)
            self.console.print_json(data=data)
        except Exception as e:
            raise ConsoleDisplayError(f"Error displaying JSON: {e!s}") from e

    # Progress tracking
    @contextmanager
    def progress(self, message: str = "Processing...") -> Generator[Progress, None, None]:
        """Show progress indicator"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=self.console,
        ) as progress:
            task = progress.add_task(message)
            yield progress
            progress.update(task, completed=True)

    # File operations
    def save_json(self, data: JSONValue, path: Union[str, Path]) -> None:
        """Save data to JSON file"""
        try:
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            self.success(f"Saved to {path}")
        except Exception as e:
            raise ConsoleDisplayError(f"Error saving JSON: {e!s}") from e

    def load_json(self, path: Union[str, Path]) -> JSONValue:
        """Load data from JSON file"""
        try:
            with open(path) as f:
                return json.load(f)
        except Exception as e:
            raise ConsoleDisplayError(f"Error loading JSON: {e!s}") from e

    def save_yaml(self, data: JSONValue, path: Union[str, Path]) -> None:
        """Save data to YAML file"""
        try:
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as f:
                yaml.dump(data, f)
            self.success(f"Saved to {path}")
        except Exception as e:
            raise ConsoleDisplayError(f"Error saving YAML: {e!s}") from e

    def load_yaml(self, path: Union[str, Path]) -> JSONValue:
        """Load data from YAML file"""
        try:
            with open(path) as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise ConsoleDisplayError(f"Error loading YAML: {e!s}") from e
