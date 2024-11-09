from pepperpy.core import BaseModule

from .console import Console


class ConsoleModule(BaseModule):
    __module_name__ = "console"

    async def setup(self) -> None:
        """Initialize console module."""
        self.console = Console()

    async def cleanup(self) -> None:
        """Cleanup console resources."""
        pass
