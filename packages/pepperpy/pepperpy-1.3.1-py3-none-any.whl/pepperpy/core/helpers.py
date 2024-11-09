"""Common utility functions and helpers"""

import json
import logging
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Optional, Type, TypeVar

import yaml

T = TypeVar("T")


def load_config(path: Path) -> Dict[str, Any]:
    """
    Load configuration from file (supports JSON and YAML)

    Args:
        path: Path to configuration file

    Returns:
        Dict containing configuration data
    """
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    try:
        if path.suffix in [".yaml", ".yml"]:
            with path.open("r") as f:
                return yaml.safe_load(f)
        elif path.suffix == ".json":
            with path.open("r") as f:
                return json.load(f)
        else:
            raise ValueError(f"Unsupported config format: {path.suffix}")
    except Exception as e:
        logging.getLogger(__name__).error(f"Failed to load config: {e}")
        raise


def serialize_datetime(obj: Any) -> str:
    """Convert datetime objects to ISO format strings"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def deep_merge(base: Dict, update: Dict) -> Dict:
    """
    Deep merge two dictionaries

    Args:
        base: Base dictionary
        update: Dictionary to merge on top

    Returns:
        Merged dictionary
    """
    result = base.copy()

    for key, value in update.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value

    return result


def safe_cast(value: Any, target_type: Type[T], default: Optional[T] = None) -> Optional[T]:
    """
    Safely cast value to target type

    Args:
        value: Value to cast
        target_type: Type to cast to
        default: Default value if cast fails

    Returns:
        Cast value or default
    """
    try:
        return target_type(value)
    except (ValueError, TypeError):
        return default
