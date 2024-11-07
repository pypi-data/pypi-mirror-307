"""
PepperPy - Python Development Accelerator
"""

from .console import Console, ConsoleTemplates, OutputFormat, Style
from .core import Application, Config, Context, Module, PepperError

__version__ = "0.1.0"

__all__ = [
    "Application",
    "Config",
    "Context",
    "Module",
    "PepperError",
    "Console",
    "ConsoleTemplates",
    "OutputFormat",
    "Style",
]
