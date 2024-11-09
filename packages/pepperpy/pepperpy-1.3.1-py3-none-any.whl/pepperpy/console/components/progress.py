"""Progress and status indicators for console output"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

from rich.progress import BarColumn, SpinnerColumn, TaskID, TextColumn, TimeRemainingColumn
from rich.progress import Progress as RichProgress
from rich.status import Status as RichStatus
from rich.style import Style as RichStyle


@dataclass
class ProgressConfig:
    """Progress bar configuration"""

    description: str
    total: float = 100.0
    style: Optional[str] = None
    show_percentage: bool = True
    show_time: bool = True
    show_spinner: bool = True
    auto_refresh: bool = True


class Progress:
    """Enhanced progress bar wrapper"""

    def __init__(self, console, config: Optional[ProgressConfig] = None):
        """Initialize progress bar.

        Args:
            console: Console instance
            config: Optional progress configuration
        """
        self.config = config or ProgressConfig(description="Processing...")

        # Build columns based on configuration
        columns = []
        if self.config.show_spinner:
            columns.append(SpinnerColumn())

        columns.extend(
            [
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
            ]
        )

        if self.config.show_percentage:
            columns.append(TextColumn("[progress.percentage]{task.percentage:>3.0f}%"))

        if self.config.show_time:
            columns.append(TimeRemainingColumn())

        self._progress = RichProgress(
            *columns, console=console, auto_refresh=self.config.auto_refresh
        )
        self._tasks: Dict[str, TaskID] = {}

    def add_task(
        self,
        description: str,
        total: Optional[float] = None,
        style: Optional[Union[str, RichStyle]] = None,
    ) -> TaskID:
        """Add a new task to the progress bar.

        Args:
            description: Task description
            total: Total steps for the task
            style: Optional style for the task

        Returns:
            TaskID: Identifier for the created task
        """
        task_id = self._progress.add_task(
            description, total=total or self.config.total, style=style or self.config.style
        )
        self._tasks[description] = task_id
        return task_id

    def update(
        self, task_id: Union[TaskID, str], advance: Optional[float] = None, **kwargs: Any
    ) -> None:
        """Update task progress.

        Args:
            task_id: Task identifier or description
            advance: Amount to advance the task
            **kwargs: Additional task fields to update
        """
        if isinstance(task_id, str):
            task_id = self._tasks.get(task_id)
            if task_id is None:
                raise KeyError(f"Task '{task_id}' not found")

        self._progress.update(task_id, advance=advance, **kwargs)

    def remove_task(self, task_id: Union[TaskID, str]) -> None:
        """Remove a task from the progress bar.

        Args:
            task_id: Task identifier or description
        """
        if isinstance(task_id, str):
            task_id = self._tasks.pop(task_id, None)
            if task_id is None:
                return

        self._progress.remove_task(task_id)

    def start(self) -> None:
        """Start the progress display."""
        self._progress.start()

    def stop(self) -> None:
        """Stop the progress display."""
        self._progress.stop()

    def __enter__(self) -> "Progress":
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.stop()


class Status:
    """Enhanced status indicator"""

    def __init__(self, console):
        """Initialize status indicator.

        Args:
            console: Console instance
        """
        self._status = RichStatus(console=console)
        self._current: Optional[str] = None

    def update(self, status: str, style: Optional[Union[str, RichStyle]] = None) -> None:
        """Update status message.

        Args:
            status: New status message to display
            style: Optional style for the status
        """
        self._current = status
        self._status.update(status, style=style)

    def start(self, status: str, style: Optional[Union[str, RichStyle]] = None) -> None:
        """Start displaying status.

        Args:
            status: Initial status message
            style: Optional style for the status
        """
        self._current = status
        self._status.start(status, style=style)

    def stop(self) -> None:
        """Stop displaying status."""
        self._status.stop()

    def __enter__(self) -> "Status":
        """Context manager entry."""
        if self._current:
            self.start(self._current)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.stop()
