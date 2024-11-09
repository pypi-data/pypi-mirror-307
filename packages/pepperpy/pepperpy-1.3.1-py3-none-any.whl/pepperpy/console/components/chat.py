"""Chat interface component"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.style import Style


@dataclass
class Message:
    """Chat message"""

    content: str
    sender: str
    timestamp: datetime = datetime.now()
    style: Optional[str] = None


class Chat:
    """Interactive chat interface"""

    def __init__(self, console: Console, title: str = "Chat", theme: str = "dark"):
        """Initialize chat interface.

        Args:
            console: Console instance
            title: Chat title
            theme: Chat theme
        """
        self._console = console
        self._title = title
        self._theme = theme
        self._messages = []

    async def add_message(self, content: str, sender: str, style: Optional[Style] = None) -> None:
        """Add message to chat.

        Args:
            content: Message content
            sender: Message sender
            style: Optional message style
        """
        message = Message(content=content, sender=sender, style=style.value if style else None)
        self._messages.append(message)
        self._render_message(message)

    def _render_message(self, message: Message) -> None:
        """Render single message.

        Args:
            message: Message to render
        """
        # Criar cabeçalho com timestamp
        header = f"[{message.sender}] {message.timestamp:%H:%M:%S}"

        # Criar painel com a mensagem
        panel = Panel(
            message.content,
            title=header,
            style=message.style,
            border_style="dim" if self._theme == "dark" else None,
        )

        self._console.print(panel)

    def clear(self) -> None:
        """Clear chat history."""
        self._messages.clear()
        self._console.clear()
