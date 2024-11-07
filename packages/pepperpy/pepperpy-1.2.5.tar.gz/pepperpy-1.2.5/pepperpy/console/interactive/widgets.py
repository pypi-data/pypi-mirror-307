import calendar
from datetime import date
from typing import List, Optional

import questionary
from rich.console import Console


class InteractiveWidgets:
    """Advanced interactive console widgets"""

    def __init__(self, console: Console) -> None:
        self.console = console

    async def search_select(
        self, choices: List[str], message: str = "Search:", min_chars: int = 2
    ) -> str:
        """Interactive searchable selection"""
        return await questionary.autocomplete(
            message,
            choices=choices,
            validate=lambda x: len(x) >= min_chars,
            match_middle=True,
        ).ask_async()

    async def date_picker(
        self,
        message: str = "Select date:",
        min_date: Optional[date] = None,
        max_date: Optional[date] = None,
    ) -> date:
        """Interactive date picker"""
        today = date.today()
        year = await questionary.select(
            "Year:",
            choices=[
                str(y)
                for y in range(
                    min_date.year if min_date else today.year - 10,
                    max_date.year if max_date else today.year + 10,
                )
            ],
        ).ask_async()

        month = await questionary.select(
            "Month:", choices=[f"{m:02d}" for m in range(1, 13)]
        ).ask_async()

        # Get valid days for selected month/year
        _, last_day = calendar.monthrange(int(year), int(month))
        day = await questionary.select(
            "Day:", choices=[f"{d:02d}" for d in range(1, last_day + 1)]
        ).ask_async()

        return date(int(year), int(month), int(day))

    async def color_picker(
        self, message: str = "Select color:", palette: Optional[List[str]] = None
    ) -> str:
        """Interactive color picker"""
        default_palette = [
            "#ff0000",
            "#00ff00",
            "#0000ff",
            "#ffff00",
            "#ff00ff",
            "#00ffff",
        ]

        colors = palette or default_palette
        color_names = {
            "#ff0000": "Red",
            "#00ff00": "Green",
            "#0000ff": "Blue",
            "#ffff00": "Yellow",
            "#ff00ff": "Magenta",
            "#00ffff": "Cyan",
        }

        # Show color preview
        for color in colors:
            name = color_names.get(color, color)
            self.console.print("■", style=f"rgb({color})", end=" ")
            self.console.print(name)

        return await questionary.select(message, choices=colors).ask_async()

    async def tag_input(
        self,
        message: str = "Enter tags:",
        suggestions: Optional[List[str]] = None,
        max_tags: Optional[int] = None,
    ) -> List[str]:
        """Interactive tag input"""
        tags = []
        while True:
            if max_tags and len(tags) >= max_tags:
                break

            tag = await questionary.autocomplete(
                f"{message} ({len(tags)} tags)",
                choices=suggestions or [],
                validate=lambda x: x not in tags,
                ignore_case=True,
            ).ask_async()

            if not tag:
                break

            tags.append(tag)
            self.console.print(f"Added tag: {tag}")

            if not await questionary.confirm("Add another tag?").ask_async():
                break

        return tags
