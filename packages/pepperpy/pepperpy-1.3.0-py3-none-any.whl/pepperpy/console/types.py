from enum import Enum
from pathlib import Path
from typing import Dict, TypedDict, Union

# Tipos básicos
ConsoleData = Union[str, int, float, bool, dict, list, None]
PathLike = Union[str, Path]


# Formatos suportados
class OutputFormat(str, Enum):
    AUTO = "auto"
    JSON = "json"
    YAML = "yaml"
    TABLE = "table"
    TEXT = "text"


# Estilos
class Style(str, Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    HIGHLIGHT = "highlight"
    MUTED = "muted"
    CODE = "code"
    DATA = "data"
    URL = "url"


# Configurações
class ConsoleConfig(TypedDict, total=False):
    theme: Dict[str, str]
    timestamp_format: str
    default_style: str
    show_timestamps: bool
