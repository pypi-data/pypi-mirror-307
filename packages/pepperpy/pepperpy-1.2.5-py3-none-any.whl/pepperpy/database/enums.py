from enum import Enum, auto


class DatabaseBackendType(str, Enum):
    """Supported database backends"""

    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    DUCKDB = "duckdb"


class TransactionIsolationLevel(str, Enum):
    """Transaction isolation levels"""

    READ_UNCOMMITTED = "READ UNCOMMITTED"
    READ_COMMITTED = "READ COMMITTED"
    REPEATABLE_READ = "REPEATABLE READ"
    SERIALIZABLE = "SERIALIZABLE"


class CacheStrategy(str, Enum):
    """Cache strategies"""

    NONE = "none"
    MEMORY = "memory"
    REDIS = "redis"


class ModelState(str, Enum):
    """Model instance states"""

    NEW = auto()
    LOADED = auto()
    MODIFIED = auto()
    DELETED = auto()
