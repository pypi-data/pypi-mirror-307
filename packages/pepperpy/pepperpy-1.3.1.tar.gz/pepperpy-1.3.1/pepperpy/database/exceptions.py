"""Database-specific exceptions"""

from pepperpy.core.exceptions import DatabaseError


class MigrationError(DatabaseError):
    """Raised when database migration fails"""

    pass
