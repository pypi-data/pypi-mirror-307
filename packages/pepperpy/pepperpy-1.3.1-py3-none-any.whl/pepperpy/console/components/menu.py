import asyncio
import inspect
from contextlib import suppress
from dataclasses import dataclass
from typing import Any, Callable, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt


@dataclass
class MenuItem:
    """Menu item configuration"""

    label: str
    action: Callable[[], Any]
    description: Optional[str] = None
    shortcut: Optional[str] = None
    enabled: bool = True
    separator_before: bool = False
    separator_after: bool = False


class Menu:
    """Interactive menu component with rich formatting"""

    def __init__(self, console: Console, title: Optional[str] = None, style: Optional[str] = None):
        """Initialize menu component."""
        self._console = console
        self._title = title
        self._style = style
        self._items: List[MenuItem] = []
        self._running = True

    def add_item(
        self,
        label: str,
        action: Callable[[], Any],
        description: Optional[str] = None,
        shortcut: Optional[str] = None,
        enabled: bool = True,
    ) -> None:
        """Add menu item."""
        item = MenuItem(
            label=label, action=action, description=description, shortcut=shortcut, enabled=enabled
        )
        self._items.append(item)

    def add_separator(self) -> None:
        """Add separator between items."""
        if self._items:
            self._items[-1].separator_after = True

    def clear(self) -> None:
        """Clear all menu items."""
        self._items.clear()

    async def _execute_action(self, action: Callable[[], Any]) -> Any:
        """Execute action handling both sync and async functions."""
        try:
            if inspect.iscoroutinefunction(action):
                return await action()
            return action()
        except (KeyboardInterrupt, asyncio.CancelledError):
            self._running = False
            self._console.print("\n[yellow]Action cancelled[/]")
            return None

    async def show(self) -> Any:
        """Display menu and handle selection."""
        try:
            while self._running:
                # Display menu title
                if self._title:
                    self._console.print(Panel(self._title, style=self._style or "bold blue"))

                # Display items
                for idx, item in enumerate(self._items, 1):
                    if item.separator_before:
                        self._console.print("─" * 40)

                    prefix = f"{idx}."
                    if item.shortcut:
                        prefix = f"{prefix} [{item.shortcut}]"

                    label = f"{prefix} {item.label}"
                    if not item.enabled:
                        label = f"[dim]{label}[/]"

                    self._console.print(label)

                    if item.description:
                        self._console.print(f"   [dim]{item.description}[/]")

                    if item.separator_after:
                        self._console.print("─" * 40)

                # Get selection
                try:
                    choice = Prompt.ask(
                        "Select an option", choices=[str(i) for i in range(1, len(self._items) + 1)]
                    )

                    # Execute selected action
                    item = self._items[int(choice) - 1]
                    if not item.enabled:
                        self._console.print("[red]This option is disabled[/]")
                        continue

                    result = await self._execute_action(item.action)

                    # Ask if user wants to continue
                    if self._running and not Prompt.ask(
                        "Would you like to perform another action?", default=True
                    ):
                        return result

                except (ValueError, IndexError):
                    self._console.print("[red]Invalid selection[/]")
                    continue

        except (KeyboardInterrupt, asyncio.CancelledError):
            with suppress(Exception):
                self._console.print("\n[yellow]Menu cancelled[/]")
            return None
