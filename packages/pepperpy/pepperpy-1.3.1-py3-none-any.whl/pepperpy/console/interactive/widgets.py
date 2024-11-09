from datetime import datetime
from typing import List, Optional

from rich.console import Console as RichConsole


class InteractiveWidgets:
    def __init__(self, console: RichConsole) -> None:
        self.console = console

    async def date_picker(self, message: str) -> datetime:
        """Simple date picker implementation."""
        while True:
            try:
                date_str = input(f"{message} (YYYY-MM-DD) > ")
                return datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                self.console.print("[red]Invalid date format. Please use YYYY-MM-DD[/]")

    async def tag_input(self, message: str, suggestions: Optional[List[str]] = None) -> List[str]:
        """Tag input with suggestions."""
        if suggestions:
            self.console.print(f"Suggestions: {', '.join(suggestions)}")

        tags_input = input(f"{message} (comma-separated) > ")
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        return tags
