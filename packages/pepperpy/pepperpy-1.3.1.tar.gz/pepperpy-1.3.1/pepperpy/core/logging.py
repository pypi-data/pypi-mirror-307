import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Union

from rich.console import Console as RichConsole
from rich.logging import RichHandler


class LogLevel(str, Enum):
    """Log levels with string values for easy configuration"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    def __str__(self) -> str:
        return self.value


@dataclass
class LogConfig:
    """Logging configuration"""

    level: Union[LogLevel, str] = LogLevel.INFO
    file: Optional[Union[str, Path]] = None
    format: str = "%(message)s"
    date_format: str = "[%X]"
    rich_console: bool = True
    show_path: bool = False
    show_time: bool = True
    show_level: bool = True

    def __post_init__(self):
        """Convert level to string if it's an enum"""
        if isinstance(self.level, LogLevel):
            self.level = str(self.level)


class PepperLogger:
    """Simplified logging interface for PepperPy"""

    # Configuração padrão para toda a lib
    DEFAULT_CONFIG = LogConfig(
        level=LogLevel.INFO,
        rich_console=True,
        show_time=True,
        show_level=True,
    )

    _instances = {}

    def __init__(self, name: str, config: Optional[LogConfig] = None):
        self.name = name
        self.config = config or self.DEFAULT_CONFIG
        self._console = RichConsole()
        self._logger = self._setup_logger()

    @classmethod
    def get(cls, name: str) -> "PepperLogger":
        """Get or create a logger instance using default configuration"""
        if name not in cls._instances:
            cls._instances[name] = cls(name)
        return cls._instances[name]

    @classmethod
    def configure(cls, name: str, config: LogConfig) -> "PepperLogger":
        """Create or reconfigure a logger instance with custom configuration"""
        cls._instances[name] = cls(name, config)
        return cls._instances[name]

    def _setup_logger(self) -> logging.Logger:
        """Setup logger with configuration"""
        logger = logging.getLogger(self.name)
        logger.setLevel(self.config.level)
        logger.handlers = []  # Clear existing handlers

        # Rich console handler
        if self.config.rich_console:
            rich_handler = RichHandler(
                rich_tracebacks=True,
                show_path=self.config.show_path,
                show_time=self.config.show_time,
                show_level=self.config.show_level,
                console=self._console,
            )
            rich_handler.setFormatter(
                logging.Formatter(self.config.format, datefmt=self.config.date_format)
            )
            logger.addHandler(rich_handler)

        # File handler if specified
        if self.config.file:
            file_handler = logging.FileHandler(self.config.file)
            file_handler.setFormatter(
                logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            )
            logger.addHandler(file_handler)

        return logger

    def debug(self, message: str, *args, **kwargs) -> None:
        """Log debug message"""
        self._logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs) -> None:
        """Log info message"""
        self._logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs) -> None:
        """Log warning message"""
        self._logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs) -> None:
        """Log error message"""
        self._logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs) -> None:
        """Log critical message"""
        self._logger.critical(message, *args, **kwargs)

    def exception(self, message: str, *args, exc_info: bool = True, **kwargs) -> None:
        """Log exception with traceback"""
        self._logger.exception(message, *args, exc_info=exc_info, **kwargs)


# Função simplificada para obter logger
def get_logger(name: str) -> PepperLogger:
    """Get a logger instance with default configuration"""
    return PepperLogger.get(f"pepperpy.{name}")
