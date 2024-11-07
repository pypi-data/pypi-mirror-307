from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ModuleMetadata:
    """Module metadata information"""

    name: str
    version: str
    description: str
    author: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    settings: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)


class MetadataProvider:
    """Module metadata management"""

    def __init__(self) -> None:
        self._metadata: Dict[str, ModuleMetadata] = {}

    def register(self, metadata: ModuleMetadata) -> None:
        """Register module metadata"""
        self._metadata[metadata.name] = metadata

    def get(self, name: str) -> Optional[ModuleMetadata]:
        """Get module metadata"""
        return self._metadata.get(name)

    def list_modules(self, tag: Optional[str] = None) -> List[ModuleMetadata]:
        """List available modules"""
        if tag:
            return [m for m in self._metadata.values() if tag in m.tags]
        return list(self._metadata.values())
