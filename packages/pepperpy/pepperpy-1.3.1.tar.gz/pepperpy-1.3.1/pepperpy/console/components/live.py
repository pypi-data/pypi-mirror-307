"""Live updating display component"""

from dataclasses import dataclass
from typing import Optional

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.style import Style as RichStyle


@dataclass
class LiveUpdate:
    """Live update content configuration"""

    content: str
    title: Optional[str] = None
    style: Optional[RichStyle] = None


class LiveDisplay:
    """Enhanced live display component"""

    def __init__(self, console: Console, auto_refresh: bool = True):
        """Initialize live display.

        Args:
            console: Console instance
            auto_refresh: Whether to auto refresh display
        """
        self._console = console
        self._live = Live(console=console, auto_refresh=auto_refresh)

    def update(
        self, content: str, title: Optional[str] = None, style: Optional[RichStyle] = None
    ) -> None:
        """Update display content.

        Args:
            content: Content to display
            title: Optional content title
            style: Optional content style
        """
        panel = Panel(content, title=title, style=style)
        self._live.update(panel)

    def start(self) -> None:
        """Start live display."""
        self._live.start()

    def stop(self) -> None:
        """Stop live display."""
        self._live.stop()

    def __enter__(self) -> "LiveDisplay":
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.stop()
