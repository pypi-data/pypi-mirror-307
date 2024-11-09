import json
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Union

from rich.box import DOUBLE
from rich.console import Console as RichConsole
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table

from .components.chat import Chat
from .components.layout import Layout as ConsoleLayout
from .components.live import LiveDisplay
from .components.menu import Menu
from .components.tree import Tree
from .components.wizard import ConfigWizard, WizardStep
from .styles import Style
from .templates import ConsoleTemplates


class Console:
    def __init__(self) -> None:
        """Initialize console with default configuration."""
        self.console = RichConsole()
        self._setup_default_templates()
        self._setup_components()

    def _setup_components(self) -> None:
        """Initialize rich components."""
        self.chat = Chat(self.console)
        self.layout = ConsoleLayout(self.console)
        self.menu = Menu(self.console)
        self._tree = Tree(self.console)
        self._config_wizard = ConfigWizard(self.console)

    def _setup_default_templates(self) -> None:
        """Setup default message templates."""
        ConsoleTemplates.add("info", "[blue]$message[/]")
        ConsoleTemplates.add("success", "[green]✓ $message[/]")
        ConsoleTemplates.add("warning", "[yellow]⚠ $message[/]")
        ConsoleTemplates.add("error", "[red]✖ $message[/]")

    def print(self, message: str, style: Optional[Style] = None) -> None:
        """Print message with optional style."""
        self.console.print(message, style=style.value if style else None)

    def title(self, text: str) -> None:
        """Display a title."""
        self.console.print(f"\n[bold white]{text}[/]\n")

    def info(self, message: str) -> None:
        """Display info message."""
        self.print(ConsoleTemplates.get("info", message=message))

    def success(self, message: str) -> None:
        """Display success message."""
        self.print(ConsoleTemplates.get("success", message=message))

    def warning(self, message: str) -> None:
        """Display warning message."""
        self.print(ConsoleTemplates.get("warning", message=message))

    def error(self, message: str) -> None:
        """Display error message."""
        self.print(ConsoleTemplates.get("error", message=message))

    def table(self, data: List[Dict[str, Any]], title: Optional[str] = None) -> None:
        """Display data in table format."""
        if not data:
            return

        table = Table(title=title)
        columns = data[0].keys()

        for column in columns:
            table.add_column(str(column))

        for row in data:
            table.add_row(*[str(row[col]) for col in columns])

        self.console.print(table)

    def show(self, data: Any, title: Optional[str] = None) -> None:
        """Display data in pretty format."""
        if title:
            self.title(title)
        self.console.print(data)

    def ask(
        self, message: str, choices: Optional[List[str]] = None, default: Optional[str] = None
    ) -> str:
        """Get user input with optional choices."""
        if choices:
            choices_str = f" ({'/'.join(choices)})"
            message = f"{message}{choices_str}"

        while True:
            response = input(f"{message} > ").strip()

            if not response and default:
                return default

            if not choices or response in choices:
                return response

            self.error(f"Please choose from: {', '.join(choices)}")

    def confirm(self, message: str, default: bool = True) -> bool:
        """Get yes/no confirmation from user."""
        suffix = " [Y/n]" if default else " [y/N]"
        response = input(f"{message}{suffix} ").strip().lower()

        if not response:
            return default

        return response[0] == "y"

    @contextmanager
    def progress(self, description: str) -> Generator[Progress, None, None]:
        """Create a progress bar context manager.

        Args:
            description: Progress bar description

        Yields:
            Progress: Progress bar instance with task already created
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console,
        )

        try:
            with progress:
                # Criar a task automaticamente com total=1.0 para trabalhar com porcentagens
                task_id = progress.add_task(description, total=1.0)
                # Envolver a task_id com o progress para facilitar o uso
                progress.task_id = task_id
                yield progress
        finally:
            pass

    def save_json(self, data: Any, path: Union[str, Path]) -> None:
        """Save data as JSON file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w") as f:
            json.dump(data, f, indent=2, default=str)

    def clear(self) -> None:
        """Clear the console screen."""
        self.console.clear()

    def log(self, message: str) -> None:
        """Log a message with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.print(f"[dim]{timestamp}[/] {message}")

    def divider(self) -> None:
        """Print a divider line."""
        self.console.print("─" * 80)

    def markdown(self, text: str) -> None:
        """Render markdown text."""
        md = Markdown(text)
        self.console.print(md)

    def syntax(self, code: str, language: str = "python") -> None:
        """Display syntax-highlighted code."""
        syntax = Syntax(code, language, theme="monokai")
        self.console.print(syntax)

    def panel(
        self,
        content: str,
        title: Optional[str] = None,
        style: Optional[Style] = None,
        border_style: Optional[Style] = None,
        padding: tuple[int, int] = (1, 2),
    ) -> None:
        """Display content in a panel.

        Args:
            content: Panel content
            title: Optional panel title
            style: Optional content style
            border_style: Optional border style
            padding: Panel padding (vertical, horizontal)
        """
        panel = Panel(
            content,
            title=title,
            style=style.value if style else None,
            border_style=border_style.value if border_style else None,
            padding=padding,
        )
        self.console.print(panel)

    @contextmanager
    def live(self, auto_refresh: bool = True) -> Generator[Live, None, None]:
        """Create live-updating display context."""
        with Live(console=self.console, auto_refresh=auto_refresh) as live:
            yield live

    async def wizard_prompt(self, title: str, steps: List[WizardStep]) -> Dict[str, Any]:
        """Run configuration wizard."""
        return await self.wizard.run(title, steps)

    def tree(
        self, data: Dict[str, Any], title: Optional[str] = None, style: Optional[Style] = None
    ) -> None:
        """Display hierarchical data as tree.

        Args:
            data: Data to display
            title: Optional tree title
            style: Optional tree style
        """
        self._tree.render(data=data, title=title, style=style.value if style else None)

    async def menu_prompt(
        self, title: str, options: Dict[str, Any], description: Optional[str] = None
    ) -> Any:
        """Display interactive menu."""
        return await self.menu.show(title, options, description)

    def header(
        self,
        title: str,
        subtitle: Optional[str] = None,
        style: Optional[Style] = None,
        width: Optional[int] = None,
    ) -> None:
        """Display formatted header with optional subtitle.

        Args:
            title: Header title
            subtitle: Optional subtitle
            style: Optional style for header
            width: Optional width for header panel
        """
        # Criar conteúdo do painel
        content = [title]
        if subtitle:
            content.append("")  # Linha em branco para separação
            content.append(f"[dim]{subtitle}[/]")

        # Criar painel com bordas duplas
        panel = Panel(
            "\n".join(content),
            style=style.value if style else "bold blue",
            box=DOUBLE,
            width=width,
            padding=(1, 2),
        )

        # Adicionar espaçamento e exibir
        self.console.print()
        self.console.print(panel)
        self.console.print()

    async def wizard(
        self, title: str, steps: List[WizardStep], style: Optional[Style] = None
    ) -> Dict[str, Any]:
        """Run configuration wizard.

        Args:
            title: Wizard title
            steps: Configuration steps
            style: Optional style for wizard

        Returns:
            Dict[str, Any]: Collected configuration
        """
        return await self._config_wizard.run(title, steps)

    def create_chat(self, title: str, theme: str = "dark") -> Chat:
        """Create a new chat interface.

        Args:
            title: Chat title
            theme: Chat theme

        Returns:
            Chat: Chat interface instance
        """
        return Chat(self.console, title=title, theme=theme)

    def create_menu(self, title: str, style: Optional[Style] = None) -> Menu:
        """Create a new menu interface.

        Args:
            title: Menu title
            style: Optional menu style

        Returns:
            Menu: Menu interface instance
        """
        return Menu(self.console, title=title, style=style.value if style else None)

    @contextmanager
    def live_display(self) -> Generator[LiveDisplay, None, None]:
        """Create a live display context.

        Yields:
            LiveDisplay: Live display instance
        """
        display = LiveDisplay(self.console)
        with display:
            yield display
