from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union, cast

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from typer.core import Context, TyperArgument, TyperOption

T = TypeVar("T")
CallbackType = Callable[..., Any]


@dataclass
class CommandConfig:
    """Configuration for CLI command."""

    name: str
    help: str
    callback: CallbackType
    options: List[Dict[str, Any]] = field(default_factory=list)
    arguments: List[Dict[str, Any]] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    hidden: bool = False


class CommandBuilder:
    """Builder for CLI commands."""

    def __init__(self, name: str, help_text: str = "", hidden: bool = False) -> None:
        self.config = CommandConfig(name=name, help=help_text, callback=lambda: None, hidden=hidden)

    def option(
        self,
        name: str,
        type_: Type[T] = str,
        help_text: str = "",
        default: Optional[T] = None,
        required: bool = False,
    ) -> "CommandBuilder":
        """Add command option."""
        type_ = cast(Type[T], type_)
        self.config.options.append(
            {
                "name": name,
                "type": type_,
                "help": help_text,
                "default": default,
                "required": required,
            }
        )
        return self

    def argument(
        self,
        name: str,
        type_: Type[T] = str,
        help_text: str = "",
        required: bool = True,
    ) -> "CommandBuilder":
        """Add command argument."""
        self.config.arguments.append(
            {"name": name, "type": type_, "help": help_text, "required": required}
        )
        return self

    def alias(self, *names: str) -> "CommandBuilder":
        """Add command aliases."""
        self.config.aliases.extend(names)
        return self

    def callback(self, func: CallbackType) -> CallbackType:
        """Set command callback."""
        self.config.callback = func
        return func


class CLIBuilder:
    """Builder for CLI applications."""

    def __init__(self, name: str, help_text: str = "", version: str = "0.1.0") -> None:
        self.app = typer.Typer(name=name, help=help_text, rich_markup_mode="rich")
        self.version = version
        self.console = Console()
        self._commands: Dict[str, CommandConfig] = {}

        @self.app.callback()
        def version_callback(
            version_flag: bool = typer.Option(
                False, "--version", "-v", help="Show version and exit"
            ),
        ) -> None:
            if version_flag:
                self.console.print(f"{name} version: {self.version}")
                raise typer.Exit()

        self._version_callback = version_callback

    def command(
        self,
        name: Optional[str | CallbackType] = None,
        help_text: str = "",
        hidden: bool = False,
    ) -> Union[CommandBuilder, Callable[[CallbackType], CallbackType]]:
        """Create new command."""

        def decorator(func: CallbackType) -> CallbackType:
            cmd_name = name if isinstance(name, str) else func.__name__
            builder = CommandBuilder(cmd_name, help_text, hidden)

            @wraps(func)
            def wrapper(
                ctx: typer.Context, **kwargs: Dict[str, str | int | float | bool]
            ) -> Union[str, int, float, bool, None]:
                return func(ctx, **kwargs)

            builder.callback(wrapper)
            self._commands[cmd_name] = builder.config

            cmd = typer.Command(
                name=cmd_name,
                help=help_text,
                callback=self._wrap_callback(wrapper),
                hidden=hidden,
            )

            self.app.command()(cmd)
            return wrapper

        if callable(name):
            func = name
            name = None
            return decorator(func)
        return decorator

    def _wrap_callback(self, func: Callable) -> Callable:
        """Wrap command callback with progress and error handling"""

        async def wrapper(
            ctx: Context,
            *args: Union[TyperArgument, TyperOption],
            **kwargs: Union[str, int, float, bool],
        ) -> Union[str, int, float, bool, None]:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
            ) as progress:
                try:
                    task = progress.add_task(f"Running {func.__name__}...", total=None)
                    result = await func(*args, **kwargs)
                    progress.update(task, completed=True)
                    return result
                except Exception as err:
                    self.console.print(f"[red]Error:[/red] {err!s}")
                    raise typer.Exit(1) from err

        return wrapper

    def build(self) -> typer.Typer:
        """Build CLI application"""
        return self.app
