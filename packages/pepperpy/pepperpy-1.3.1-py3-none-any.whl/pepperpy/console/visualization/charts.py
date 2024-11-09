from dataclasses import dataclass
from typing import Dict, List

from rich.console import Console as RichConsole


@dataclass
class ChartTheme:
    background: str
    foreground: str
    accent: str


class ConsoleCharts:
    def __init__(self, console: RichConsole, theme: ChartTheme) -> None:
        self.console = console
        self.theme = theme

    def line_chart(
        self, data: Dict[str, List[float]], title: str, width: int = 60, height: int = 20
    ) -> None:
        """Display line chart in console."""
        self.console.print(f"\n[bold]{title}[/]")
        # Simplified ASCII chart implementation
        for series_name, values in data.items():
            max_val = max(values)
            normalized = [int((v / max_val) * (width - 10)) for v in values]
            self.console.print(f"\n{series_name}:")
            self.console.print("█" * normalized[-1])

    def histogram(self, data: List[float], bins: int, title: str) -> None:
        """Display histogram in console."""
        self.console.print(f"\n[bold]{title}[/]")
        # Simplified histogram implementation
        min_val, max_val = min(data), max(data)
        bin_size = (max_val - min_val) / bins

        counts = [0] * bins
        for value in data:
            bin_idx = min(int((value - min_val) / bin_size), bins - 1)
            counts[bin_idx] += 1

        max_count = max(counts)
        for count in counts:
            bar_length = int((count / max_count) * 40)
            self.console.print("█" * bar_length)
