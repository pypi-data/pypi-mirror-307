from dataclasses import dataclass
from typing import Dict, List, Optional, Union

import plotext as plt
from rich.console import Console


@dataclass
class ChartTheme:
    """Theme configuration for charts"""

    background: str = "#1a1a1a"
    foreground: str = "#ffffff"
    accent: str = "#00ff00"
    grid: str = "#333333"
    text: str = "#cccccc"


class ConsoleCharts:
    """Advanced console charting capabilities"""

    def __init__(self, console: Console, theme: Optional[ChartTheme] = None) -> None:
        self.console = console
        self.theme = theme or ChartTheme()

    def line_chart(
        self,
        data: Dict[str, List[Union[int, float]]],
        title: str,
        width: int = 60,
        height: int = 20,
    ) -> None:
        """Draw multi-line chart"""
        plt.clf()
        plt.theme(self.theme.background)

        for label, values in data.items():
            plt.plot(values, label=label)

        plt.title(title)
        plt.plotsize(width, height)
        plt.grid(True, self.theme.grid)
        plt.show()

    def scatter_plot(
        self,
        x: List[Union[int, float]],
        y: List[Union[int, float]],
        labels: Optional[List[str]] = None,
        title: str = "",
        width: int = 60,
        height: int = 20,
    ) -> None:
        """Draw scatter plot"""
        plt.clf()
        plt.theme(self.theme.background)
        plt.scatter(x, y, label=labels if labels else None)
        plt.title(title)
        plt.plotsize(width, height)
        plt.grid(True, self.theme.grid)
        plt.show()

    def heatmap(
        self,
        data: List[List[float]],
        x_labels: Optional[List[str]] = None,
        y_labels: Optional[List[str]] = None,
        title: str = "",
        width: int = 60,
        height: int = 20,
    ) -> None:
        """Draw heatmap"""
        plt.clf()
        plt.theme(self.theme.background)
        plt.colormap(data, x_labels, y_labels)
        plt.title(title)
        plt.plotsize(width, height)
        plt.show()

    def histogram(
        self,
        data: List[Union[int, float]],
        bins: int = 10,
        title: str = "",
        width: int = 60,
        height: int = 20,
    ) -> None:
        """Draw histogram"""
        plt.clf()
        plt.theme(self.theme.background)
        plt.hist(data, bins)
        plt.title(title)
        plt.plotsize(width, height)
        plt.grid(True, self.theme.grid)
        plt.show()

    def box_plot(
        self,
        data: List[List[Union[int, float]]],
        labels: Optional[List[str]] = None,
        title: str = "",
        width: int = 60,
        height: int = 20,
    ) -> None:
        """Draw box plot"""
        plt.clf()
        plt.theme(self.theme.background)
        plt.boxplot(data, labels)
        plt.title(title)
        plt.plotsize(width, height)
        plt.grid(True, self.theme.grid)
        plt.show()
