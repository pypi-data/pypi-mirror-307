"""PepperPy Database Module"""

from .module import Base, DatabaseModule

# Provide default instance for simple usage
database = DatabaseModule()

__all__ = ["DatabaseModule", "database", "Base"]
