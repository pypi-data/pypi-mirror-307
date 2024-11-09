"""Enhanced exception system with detailed error information"""

import traceback
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class ErrorContext:
    """Detailed error context information"""

    timestamp: datetime = datetime.now()
    module: Optional[str] = None
    operation: Optional[str] = None
    details: Dict[str, Any] = None
    traceback: Optional[str] = None


class PepperPyError(Exception):
    """Base exception for all PepperPy errors"""

    def __init__(
        self,
        message: str,
        *args,
        module: Optional[str] = None,
        operation: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
    ):
        super().__init__(message, *args)
        self.context = ErrorContext(
            module=module,
            operation=operation,
            details=details or {},
            traceback=traceback.format_exc() if cause else None,
        )
        self.__cause__ = cause


class ModuleError(PepperPyError):
    """Base exception for module-related errors"""

    pass


class ConfigurationError(PepperPyError):
    """Error in module or application configuration"""

    pass


class DependencyError(PepperPyError):
    """Error in module dependencies"""

    pass


class InitializationError(PepperPyError):
    """Error during module or application initialization"""

    pass


class ValidationError(PepperPyError):
    """Error in data validation"""

    pass


class DatabaseError(PepperPyError):
    """Database-related errors"""

    pass


class CacheError(PepperPyError):
    """Cache-related errors"""

    pass


class WebError(PepperPyError):
    """Web-related errors"""

    pass


class MediaError(PepperPyError):
    """Media processing errors"""

    pass


class SecurityError(PepperPyError):
    """Security-related errors"""

    pass


class ResourceError(PepperPyError):
    """Resource handling errors"""

    pass


class NetworkError(PepperPyError):
    """Network-related errors"""

    pass


class SerializationError(PepperPyError):
    """Data serialization errors"""

    pass


class AuthenticationError(SecurityError):
    """Authentication failures"""

    pass


class AuthorizationError(SecurityError):
    """Authorization failures"""

    pass


class RateLimitError(SecurityError):
    """Rate limit exceeded"""

    pass


class TimeoutError(NetworkError):
    """Operation timeout"""

    pass


class ConnectionError(NetworkError):
    """Connection failures"""

    pass


class ApplicationError(Exception):
    """Base exception for PepperPy application errors."""

    pass


class PepperError(Exception):
    """Base exception for all Pepper errors."""

    pass


class AIError(PepperError):
    """Base exception for AI-related errors."""

    pass


class ModelNotFoundError(AIError):
    """Raised when an AI model is not found."""

    pass


def wrap_exception(
    error: Exception,
    module: Optional[str] = None,
    operation: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
) -> PepperPyError:
    """Convert external exception to PepperPyError with context"""
    message = str(error)

    if isinstance(error, PepperPyError):
        if module:
            error.context.module = module
        if operation:
            error.context.operation = operation
        if details:
            error.context.details.update(details)
        return error

    return PepperPyError(message, module=module, operation=operation, details=details, cause=error)
