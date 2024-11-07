from typing import Any, Callable, Dict, List, Optional

from rich.console import Console as RichConsole
from rich.prompt import Prompt
from rich.table import Table
from rich.theme import Theme

from ..core.logging import ContextLogger
from .exceptions import ConsoleDisplayError, ConsoleInputError
from .templates import ConsoleTemplates
from .types import ConsoleConfig, ConsoleData, Style


class Console:
    """Console simplificado para desenvolvimento rápido"""

    def __init__(self, config: Optional[ConsoleConfig] = None) -> None:
        self.config = config or ConsoleConfig(
            theme={
                Style.INFO: "cyan",
                Style.WARNING: "yellow",
                Style.ERROR: "red",
                Style.SUCCESS: "green",
                Style.HIGHLIGHT: "magenta",
                Style.MUTED: "dim white",
                Style.CODE: "blue",
                Style.DATA: "green",
                Style.URL: "underline cyan",
            },
            timestamp_format="%H:%M:%S",
            default_style=Style.INFO,
            show_timestamps=True,
        )

        self.console = RichConsole(theme=Theme(self.config["theme"]))
        self.logger = ContextLogger("console")

    def print(self, message: ConsoleData, style: Optional[Style] = None) -> None:
        """Output com estilo"""
        try:
            self.console.print(message, style=style or self.config["default_style"])
        except Exception as e:
            raise ConsoleDisplayError(f"Error printing message: {e!s}") from e

    def log(self, message: str, level: str = "info", **kwargs: str) -> None:
        """Log usando templates"""
        try:
            if kwargs:
                message = ConsoleTemplates.get(message, **kwargs)
            getattr(self.logger, level)(message)
        except Exception as e:
            raise ConsoleDisplayError(f"Error logging message: {e!s}") from e

    # Métodos de conveniência melhorados
    def info(self, message: str, **kwargs: Dict[str, str]) -> None:
        self.log(message, "info", **kwargs)

    def success(self, message: str, **kwargs: str) -> None:
        self.log(message, "info", **kwargs)

    def warning(self, message: str, **kwargs: str) -> None:
        self.log(message, "warning", **kwargs)

    def error(self, message: str, **kwargs: str) -> None:
        self.log(message, "error", **kwargs)

    # Input com validação melhorada
    def ask(
        self,
        message: str,
        choices: Optional[List[str]] = None,
        default: Optional[str] = None,
        password: bool = False,
        validator: Optional[Callable[[str], bool]] = None,
        error_message: Optional[str] = None,
    ) -> str:
        """Input com validação"""
        try:
            while True:
                value = Prompt.ask(
                    message,
                    choices=choices,
                    default=default,
                    password=password,
                    console=self.console,
                )
                if validator is None or validator(value):
                    return value
                self.error(error_message or "Invalid input")
        except KeyboardInterrupt as e:
            raise ConsoleInputError("Input cancelled by user") from e

    # ... (resto dos métodos existentes com tipagem melhorada) ...

    # Novos métodos úteis
    def table(
        self,
        data: List[Dict[str, Any]],
        columns: Optional[List[str]] = None,
        title: Optional[str] = None,
    ) -> None:
        """Cria tabela a partir de lista de dicionários"""
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

    def prompt_dict(self, schema: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Prompt para criar dicionário baseado em schema"""
        result = {}
        for key, info in schema.items():
            value = self.ask(
                message=info.get("message", f"Enter {key}"),
                default=info.get("default"),
                choices=info.get("choices"),
                validator=info.get("validator"),
                error_message=info.get("error_message"),
            )
            result[key] = value
        return result
