"""Database module constants"""


class DatabaseEvents:
    """Database event names"""

    # Module lifecycle
    READY = "database.ready"
    ERROR = "database.error"

    # Model events
    MODEL_CREATED = "database.model.created"
    MODEL_UPDATED = "database.model.updated"
    MODEL_DELETED = "database.model.deleted"

    # Query events
    QUERY_EXECUTED = "database.query.executed"
    QUERY_ERROR = "database.query.error"

    # Transaction events
    TRANSACTION_BEGIN = "database.transaction.begin"
    TRANSACTION_COMMIT = "database.transaction.commit"
    TRANSACTION_ROLLBACK = "database.transaction.rollback"

    # Migration events
    MIGRATION_START = "database.migration.start"
    MIGRATION_COMPLETE = "database.migration.complete"
    MIGRATION_ERROR = "database.migration.error"
