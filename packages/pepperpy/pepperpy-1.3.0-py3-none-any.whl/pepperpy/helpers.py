from pathlib import Path
from typing import Dict

import requests

from .console import Console

console = Console()


def load_config(path: str) -> Dict:
    """Carrega arquivo de configuração (JSON/YAML)"""
    path = Path(path)
    if path.suffix == ".json":
        return console.load_json(path)
    elif path.suffix in (".yml", ".yaml"):
        return console.load_yaml(path)
    raise ValueError(f"Unsupported config format: {path.suffix}")


def fetch_json(url: str) -> object:
    """Faz request HTTP e retorna JSON"""
    with console.progress(f"Fetching {url}"):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


def save_data(data: object, path: str) -> None:
    """Salva dados em arquivo (formato baseado na extensão)"""
    path = Path(path)
    if path.suffix == ".json":
        console.save_json(data, path)
    elif path.suffix in (".yml", ".yaml"):
        console.save_yaml(data, path)
    else:
        raise ValueError(f"Unsupported format: {path.suffix}")


def prompt_config(schema: Dict[str, object]) -> Dict[str, object]:
    """Prompt interativo para configuração"""
    config = {}
    console.title("Configuration")
    for key, info in schema.items():
        default = info.get("default")
        value = console.ask(
            f"{info['description']} [{key}]", default=str(default) if default else None
        )
        config[key] = value
    return config
