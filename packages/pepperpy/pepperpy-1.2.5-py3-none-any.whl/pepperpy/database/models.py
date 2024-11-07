from datetime import datetime
from typing import Any, Dict, Optional, Type, TypeVar

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

T = TypeVar("T", bound="BaseModel")


class BaseModel(DeclarativeBase):
    """Base model with common functionality"""

    # Common fields
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create model instance from dictionary"""
        return cls(**data)

    def to_dict(self, exclude: Optional[set[str]] = None) -> Dict[str, Any]:
        """Convert model to dictionary"""
        exclude = exclude or set()
        return {
            c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in exclude
        }

    def update(self, data: Dict[str, Any]) -> None:
        """Update model attributes"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
