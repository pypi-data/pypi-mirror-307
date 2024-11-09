"""Animated spinner and progress indicators"""

from dataclasses import dataclass
from typing import Optional

from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner as RichSpinner
from rich.style import Style as RichStyle


@dataclass
class SpinnerStyle:
    """Spinner style configuration"""

    text: str = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    speed: float = 0.1
    style: Optional[RichStyle] = None


class Spinner:
    """Enhanced spinner component"""

    DEFAULT_SPINNERS = {
        "dots": "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
        "line": "⠂-–—–-",
        "pulse": "█▉▊▋▌▍▎▏▏▎▍▌▋▊▉█",
        "points": "∙∙∙∙∙∙",
        "arc": "◜◠◝◞◡◟",
        "clock": "🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛",
    }

    def __init__(self, console: Console):
        self._console = console
        self._spinner: Optional[RichSpinner] = None
        self._live: Optional[Live] = None

    def create(
        self,
        text: str,
        spinner_type: str = "dots",
        style: Optional[str] = None,
        speed: float = 0.1,
    ) -> RichSpinner:
        """Create a new spinner.

        Args:
            text: Spinner text
            spinner_type: Type of spinner animation
            style: Optional spinner style
            speed: Animation speed

        Returns:
            RichSpinner: Configured spinner
        """
        spinner_chars = self.DEFAULT_SPINNERS.get(spinner_type, self.DEFAULT_SPINNERS["dots"])
        return RichSpinner(
            text,
            spinner_chars,
            style=style,
            speed=speed,
        )

    def start(
        self,
        text: str,
        spinner_type: str = "dots",
        style: Optional[str] = None,
    ) -> None:
        """Start spinner animation.

        Args:
            text: Spinner text
            spinner_type: Type of spinner animation
            style: Optional spinner style
        """
        self._spinner = self.create(text, spinner_type, style)
        self._live = Live(
            self._spinner,
            console=self._console,
            refresh_per_second=20,
            transient=True,
        )
        self._live.start()

    def update(self, text: str) -> None:
        """Update spinner text.

        Args:
            text: New spinner text
        """
        if self._spinner:
            self._spinner.update(text)

    def stop(self) -> None:
        """Stop spinner animation."""
        if self._live:
            self._live.stop()
