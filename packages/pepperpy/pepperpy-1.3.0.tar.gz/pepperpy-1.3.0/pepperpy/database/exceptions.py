from pepperpy.core.exceptions import PepperError


class DatabaseError(PepperError):
    """Base exception for database errors"""

    pass


class ConnectionError(DatabaseError):
    """Database connection error"""

    pass


class TransactionError(DatabaseError):
    """Transaction related error"""

    pass


class MigrationError(DatabaseError):
    """Migration related error"""

    pass


class ModelError(DatabaseError):
    """Model related error"""

    pass


class QueryError(DatabaseError):
    """Query related error"""

    pass
