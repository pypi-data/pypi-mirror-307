from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional, Type

from pepperpy.core.events import Event

from .models import BaseModel


@dataclass
class DatabaseEvent(Event):
    """Base class for database events"""

    module: str = "database"
    timestamp: datetime = datetime.utcnow()


@dataclass
class ModelEvent(DatabaseEvent):
    """Base class for model events"""

    model_type: Type[BaseModel]
    model_id: Any
    data: Dict[str, Any]


@dataclass
class ModelCreated(ModelEvent):
    """Event emitted when a model instance is created"""

    event_type: str = "model.created"


@dataclass
class ModelUpdated(ModelEvent):
    """Event emitted when a model instance is updated"""

    event_type: str = "model.updated"
    old_data: Dict[str, Any]


@dataclass
class ModelDeleted(ModelEvent):
    """Event emitted when a model instance is deleted"""

    event_type: str = "model.deleted"


@dataclass
class QueryEvent(DatabaseEvent):
    """Base class for query events"""

    query: str
    params: Optional[Dict[str, Any]] = None


@dataclass
class QueryExecuted(QueryEvent):
    """Event emitted when a query is executed"""

    event_type: str = "query.executed"
    duration: float = 0.0
    rows_affected: int = 0


@dataclass
class TransactionEvent(DatabaseEvent):
    """Base class for transaction events"""

    transaction_id: str


@dataclass
class TransactionBegin(TransactionEvent):
    """Event emitted when a transaction begins"""

    event_type: str = "transaction.begin"


@dataclass
class TransactionCommit(TransactionEvent):
    """Event emitted when a transaction is committed"""

    event_type: str = "transaction.commit"
    duration: float = 0.0


@dataclass
class TransactionRollback(TransactionEvent):
    """Event emitted when a transaction is rolled back"""

    event_type: str = "transaction.rollback"
    error: Optional[Exception] = None
