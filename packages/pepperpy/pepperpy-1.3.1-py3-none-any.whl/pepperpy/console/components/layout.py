from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from rich.console import Console
from rich.layout import Layout as RichLayout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..styles import Style


@dataclass
class Section:
    """Layout section configuration"""

    name: str
    parent: Optional[str] = None
    ratio: Optional[int] = None
    minimum_size: Optional[int] = None
    content: Optional[Union[str, Panel, Table]] = None
    style: Optional[Style] = None


@dataclass
class LayoutConfig:
    """Layout configuration"""

    sections: Dict[str, Section] = field(default_factory=dict)
    direction: str = "vertical"
    title: Optional[str] = None
    style: Optional[Style] = None


class Layout:
    """Enhanced layout manager for terminal interfaces"""

    def __init__(self, console: Optional[Console] = None) -> None:
        """Initialize layout manager."""
        self.console = console or Console()
        self._layout = RichLayout()
        self._config = LayoutConfig()

    def _get_full_section_name(self, parent: Optional[str], name: str) -> str:
        """Get full section name including parent path."""
        return f"{parent}.{name}" if parent else name

    def _get_section_path(self, name: str) -> List[str]:
        """Get section path components."""
        return name.split(".")

    def _get_layout_section(self, name: str) -> Optional[RichLayout]:
        """Get layout section by name, handling nested sections."""
        try:
            current = self._layout
            for part in self._get_section_path(name):
                current = current[part]
            return current
        except KeyError:
            return None

    def split(self, direction: str = "vertical", sections: Optional[List[str]] = None) -> None:
        """Split layout into sections."""
        if sections:
            # Criar layouts para cada seção
            layouts = []
            for name in sections:
                layout = RichLayout(name=name)
                if direction == "vertical":
                    layout.size = len(sections)
                else:
                    layout.ratio = 1
                layouts.append(layout)
                self._config.sections[name] = Section(name=name)

            # Atualizar layout principal
            if direction == "vertical":
                self._layout.split_column(*layouts)
            else:
                self._layout.split_row(*layouts)

        self._config.direction = direction

    def split_section(self, section: str, direction: str, sections: List[str]) -> None:
        """Split an existing section into subsections."""
        parent_layout = self._get_layout_section(section)
        if not parent_layout:
            raise ValueError(f"Section '{section}' not found")

        # Criar layouts para as subseções
        sublayouts = []
        for name in sections:
            full_name = self._get_full_section_name(section, name)
            layout = RichLayout(name=name)  # Use o nome simples para o layout
            if direction == "vertical":
                layout.size = len(sections)
            else:
                layout.ratio = 1
            sublayouts.append(layout)
            self._config.sections[full_name] = Section(name=name, parent=section)

        # Atualizar seção pai
        if direction == "vertical":
            parent_layout.split_column(*sublayouts)
        else:
            parent_layout.split_row(*sublayouts)

    def add_panel(
        self, section: str, content: str, title: Optional[str] = None, style: Optional[Style] = None
    ) -> None:
        """Add panel to section."""
        layout_section = self._get_layout_section(section)
        if not layout_section:
            raise ValueError(f"Section '{section}' not found")

        panel = Panel(content, title=title, style=style.value if style else None)

        layout_section.update(panel)

    def add_stats(
        self, section: str, data: Dict[str, Union[int, float, str]], title: Optional[str] = None
    ) -> None:
        """Add statistics to section."""
        layout_section = self._get_layout_section(section)
        if not layout_section:
            raise ValueError(f"Section '{section}' not found")

        table = Table(title=title, show_header=False)
        table.add_column("Key")
        table.add_column("Value")

        for key, value in data.items():
            table.add_row(str(key), str(value))

        layout_section.update(table)

    def add_chart(
        self, section: str, data: Dict[str, List[float]], title: Optional[str] = None
    ) -> None:
        """Add chart to section."""
        layout_section = self._get_layout_section(section)
        if not layout_section:
            raise ValueError(f"Section '{section}' not found")

        # Simplified ASCII chart
        chart = []
        for series_name, values in data.items():
            max_val = max(values)
            normalized = [int((v / max_val) * 20) for v in values]
            chart.append(f"{series_name}:")
            chart.append("█" * normalized[-1])

        text = Text("\n".join(chart))
        if title:
            text = Text(f"{title}\n\n") + text

        layout_section.update(text)

    def render(self) -> None:
        """Render layout to console."""
        self.console.print(self._layout)
