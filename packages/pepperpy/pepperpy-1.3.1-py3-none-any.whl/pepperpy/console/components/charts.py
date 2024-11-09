"""Enhanced chart components for data visualization"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from rich.box import SQUARE
from rich.console import Console
from rich.style import Style as RichStyle
from rich.table import Table
from rich.text import Text


@dataclass
class ChartConfig:
    """Chart configuration"""

    width: int = 60
    height: int = 20
    style: Optional[RichStyle] = None
    show_legend: bool = True
    show_grid: bool = True
    show_values: bool = True


class Charts:
    """Enhanced chart components"""

    def __init__(self, console: Console):
        self._console = console

    def bar_chart(
        self,
        data: Dict[str, Union[int, float]],
        title: Optional[str] = None,
        config: Optional[ChartConfig] = None,
    ) -> None:
        """Display bar chart.

        Args:
            data: Data points
            title: Optional chart title
            config: Optional chart configuration
        """
        config = config or ChartConfig()
        max_value = max(data.values())
        max_label = max(len(str(k)) for k in data.keys())

        table = Table(
            title=title,
            box=SQUARE if config.show_grid else None,
            show_header=False,
            width=config.width + max_label + 4,
        )

        table.add_column("Label", style="cyan", width=max_label)
        table.add_column("Bar")
        if config.show_values:
            table.add_column("Value", style="green")

        for label, value in data.items():
            bar_width = int((value / max_value) * config.width)
            bar = "█" * bar_width
            row = [label, Text(bar, style=config.style)]
            if config.show_values:
                row.append(f"{value:,.2f}")
            table.add_row(*row)

        self._console.print(table)

    def sparkline(
        self,
        data: List[Union[int, float]],
        title: Optional[str] = None,
        style: Optional[RichStyle] = None,
    ) -> None:
        """Display sparkline chart.

        Args:
            data: Data points
            title: Optional chart title
            style: Optional chart style
        """
        if title:
            self._console.print(f"\n{title}")

        min_value = min(data)
        max_value = max(data)
        range_value = max_value - min_value

        if range_value == 0:
            normalized = [0] * len(data)
        else:
            normalized = [(x - min_value) / range_value for x in data]

        chars = "▁▂▃▄▅▆▇█"
        line = ""
        for value in normalized:
            index = min(int(value * (len(chars) - 1)), len(chars) - 1)
            line += chars[index]

        self._console.print(Text(line, style=style))
        if max_value != min_value:
            self._console.print(
                f"[dim]Min: {min_value:.2f} Max: {max_value:.2f} Range: {range_value:.2f}[/]"
            )
