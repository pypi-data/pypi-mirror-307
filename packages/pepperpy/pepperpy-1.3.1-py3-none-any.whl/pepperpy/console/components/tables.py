"""Enhanced table components"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Text

from rich.box import SQUARE, Box
from rich.console import Console
from rich.style import Style as RichStyle
from rich.table import Table as RichTable


@dataclass
class Column:
    """Table column configuration"""

    name: str
    header: Optional[str] = None
    style: Optional[RichStyle] = None
    width: Optional[int] = None
    justify: str = "left"
    format: Optional[str] = None


@dataclass
class TableConfig:
    """Table configuration"""

    show_header: bool = True
    show_lines: bool = True
    box: Optional[Box] = SQUARE
    title_style: Optional[RichStyle] = None
    header_style: Optional[RichStyle] = None
    row_styles: Optional[List[RichStyle]] = None
    padding: tuple[int, int] = (0, 1)


class EnhancedTable:
    """Enhanced table component"""

    def __init__(self, console: Console):
        self._console = console

    def create_table(
        self,
        data: List[Dict[str, Any]],
        columns: List[Column],
        title: Optional[str] = None,
        config: Optional[TableConfig] = None,
    ) -> None:
        """Create and display enhanced table.

        Args:
            data: Table data
            columns: Column configurations
            title: Optional table title
            config: Optional table configuration
        """
        config = config or TableConfig()
        table = RichTable(
            title=title,
            title_style=config.title_style,
            show_header=config.show_header,
            box=config.box,
            padding=config.padding,
        )

        # Add columns
        for col in columns:
            table.add_column(
                col.header or col.name,
                style=col.style,
                width=col.width,
                justify=col.justify,
                header_style=config.header_style,
            )

        # Add rows
        for row_idx, row_data in enumerate(data):
            row_style = None
            if config.row_styles:
                row_style = config.row_styles[row_idx % len(config.row_styles)]

            row_values = []
            for col in columns:
                value = row_data.get(col.name, "")
                if col.format and isinstance(value, (int, float)):
                    value = col.format.format(value)
                row_values.append(str(value))

            table.add_row(*row_values, style=row_style)

        self._console.print(table)

    def create_grid(
        self,
        data: List[Dict[str, Any]],
        columns: List[Column],
        grid_columns: int = 3,
        title: Optional[str] = None,
    ) -> None:
        """Create and display grid layout table.

        Args:
            data: Grid data
            columns: Column configurations
            grid_columns: Number of grid columns
            title: Optional grid title
        """
        if not data:
            return

        table = RichTable(
            title=title,
            show_header=False,
            box=None,
            padding=(0, 2),
        )

        for _ in range(grid_columns):
            table.add_column(justify="center")

        current_row = []
        for item in data:
            cell_table = RichTable(box=SQUARE, show_header=False)
            for col in columns:
                value = item.get(col.name, "")
                if col.format and isinstance(value, (int, float)):
                    value = col.format.format(value)
                cell_table.add_row(
                    Text(col.header or col.name, style="bold"),
                    str(value),
                    style=col.style,
                )

            current_row.append(cell_table)
            if len(current_row) == grid_columns:
                table.add_row(*current_row)
                current_row = []

        if current_row:
            # Fill remaining cells with empty strings
            while len(current_row) < grid_columns:
                current_row.append("")
            table.add_row(*current_row)

        self._console.print(table)
