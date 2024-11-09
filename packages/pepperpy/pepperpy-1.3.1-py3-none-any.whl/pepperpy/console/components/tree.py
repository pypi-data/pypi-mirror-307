from typing import Any, Dict, Optional, Union

from rich.console import Console
from rich.style import Style as RichStyle
from rich.tree import Tree as RichTree


class Tree:
    """Enhanced tree component for hierarchical data"""

    def __init__(self, console: Console):
        """Initialize tree component.

        Args:
            console: Console instance
        """
        self._console = console

    def render(
        self,
        data: Dict[str, Any],
        title: Optional[str] = None,
        style: Optional[Union[str, RichStyle]] = None,
    ) -> None:
        """Render tree visualization.

        Args:
            data: Hierarchical data to display
            title: Optional tree title
            style: Optional tree style
        """
        tree = RichTree(title or "Root", style=style)
        self._add_items(tree, data)
        self._console.print(tree)

    def _add_items(self, tree: RichTree, data: Any) -> None:
        """Recursively add items to tree.

        Args:
            tree: Current tree node
            data: Data to add
        """
        if isinstance(data, dict):
            for key, value in data.items():
                node = tree.add(str(key))
                self._add_items(node, value)
        elif isinstance(data, (list, tuple)):
            for item in data:
                if isinstance(item, (dict, list, tuple)):
                    node = tree.add("Item")
                    self._add_items(node, item)
                else:
                    tree.add(str(item))
        elif data is not None:
            tree.add(str(data))
