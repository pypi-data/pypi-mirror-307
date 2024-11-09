"""State management system with persistence support"""

import asyncio
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, TypeVar

import aiofiles

from .events import Event, EventBus
from .exceptions import StateError
from .types import Serializable

T = TypeVar("T")


@dataclass
class StateChange(Event):
    """State change event"""

    key: str
    old_value: Any
    new_value: Any
    timestamp: datetime = datetime.now()


class StateManager:
    """Central state management system"""

    def __init__(self, event_bus: Optional[EventBus] = None):
        self._state: Dict[str, Any] = {}
        self._persistent: Dict[str, bool] = {}
        self._event_bus = event_bus
        self._lock = asyncio.Lock()

    async def set(self, key: str, value: Any, persistent: bool = False) -> None:
        """Set state value"""
        async with self._lock:
            old_value = self._state.get(key)
            self._state[key] = value
            self._persistent[key] = persistent

            if self._event_bus:
                await self._event_bus.publish(
                    StateChange(
                        name="state_changed",
                        data={"key": key, "persistent": persistent},
                        key=key,
                        old_value=old_value,
                        new_value=value,
                    )
                )

    async def get(self, key: str, default: Any = None) -> Any:
        """Get state value"""
        return self._state.get(key, default)

    async def delete(self, key: str) -> None:
        """Delete state value"""
        async with self._lock:
            if key in self._state:
                old_value = self._state[key]
                del self._state[key]
                del self._persistent[key]

                if self._event_bus:
                    await self._event_bus.publish(
                        StateChange(
                            name="state_deleted",
                            data={"key": key},
                            key=key,
                            old_value=old_value,
                            new_value=None,
                        )
                    )

    async def save(self, path: Path) -> None:
        """Save state to file"""
        try:
            persistent_state = {k: v for k, v in self._state.items() if k in self._persistent_keys}
            async with aiofiles.open(path, "w") as f:
                json.dump(persistent_state, f, default=self._serialize)
        except Exception as e:
            raise StateError(f"Failed to save state: {e}") from e

    async def load(self, path: Path) -> None:
        """Load state from file"""
        try:
            async with aiofiles.open(path) as f:
                data = json.loads(await f.read())
                for key, value in data.items():
                    await self.set(key, value, persistent=True)
        except Exception as e:
            raise StateError(f"Failed to load state: {e}") from e

    def _serialize(self, obj: Any) -> Any:
        """Serialize object for storage"""
        if isinstance(obj, Serializable):
            return obj.to_dict()
        if isinstance(obj, (datetime, Path)):
            return str(obj)
        raise TypeError(f"Type {type(obj)} not serializable")
