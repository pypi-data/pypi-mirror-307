from dataclasses import dataclass, field
from typing import Callable, Dict, List, Type

from .models import BaseModel


@dataclass
class ModelHooks:
    """Hooks for model lifecycle events"""

    before_create: List[Callable] = field(default_factory=list)
    after_create: List[Callable] = field(default_factory=list)
    before_update: List[Callable] = field(default_factory=list)
    after_update: List[Callable] = field(default_factory=list)
    before_delete: List[Callable] = field(default_factory=list)
    after_delete: List[Callable] = field(default_factory=list)


class HookManager:
    """Manager for database operation hooks"""

    def __init__(self) -> None:
        self._hooks: Dict[Type[BaseModel], ModelHooks] = {}

    def register_hooks(self, model: Type[BaseModel], hooks: ModelHooks) -> None:
        """Register hooks for model"""
        self._hooks[model] = hooks

    def get_hooks(self, model: Type[BaseModel]) -> ModelHooks:
        """Get hooks for model"""
        if model not in self._hooks:
            self._hooks[model] = ModelHooks()
        return self._hooks[model]

    async def execute_hooks(
        self,
        hook_type: str,
        model: Type[BaseModel],
        instance: BaseModel,
        **kwargs: Dict[str, object],
    ) -> None:
        """Execute hooks of specified type"""
        hooks = getattr(self.get_hooks(model), hook_type, [])
        for hook in hooks:
            await hook(instance, **kwargs)
