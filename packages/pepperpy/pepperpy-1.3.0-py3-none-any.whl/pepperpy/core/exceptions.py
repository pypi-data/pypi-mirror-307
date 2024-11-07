"""Core exceptions for PepperPy."""

from datetime import UTC, datetime
from typing import Any, Dict, Optional


class PepperError(Exception):
    """Base exception with improved error context"""

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        self.message = message
        self.code = code or self.__class__.__name__
        self.details = details or {}
        self.cause = cause
        self.timestamp = datetime.now(UTC)

        super().__init__(f"{self.code}: {message}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary format"""
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "cause": str(self.cause) if self.cause else None,
        }


class ConfigError(PepperError):
    """Erro de configuração"""

    pass


class ValidationError(PepperError):
    """Erro de validação"""

    def __init__(self, message: str, field: Optional[str] = None) -> None:
        super().__init__(
            message,
            code="VALIDATION_ERROR",
            details={"field": field} if field else None,
        )


class ModuleError(PepperError):
    """Erro relacionado a módulos"""

    def __init__(self, message: str, module_name: str) -> None:
        super().__init__(message, code="MODULE_ERROR", details={"module": module_name})


class DependencyError(ModuleError):
    """Erro de dependência entre módulos"""

    pass


class StateError(PepperError):
    """Erro de estado da aplicação"""

    pass


class ResourceError(PepperError):
    """Erro relacionado a recursos"""

    pass


class OperationError(PepperError):
    """Erro em operações"""

    pass


class ContextError(PepperError):
    """Erro relacionado ao contexto da aplicação"""

    pass


class ServiceNotFoundError(ContextError):
    """Erro quando um serviço não é encontrado no contexto"""

    pass


class ApplicationStartupError(PepperError):
    """Erro durante inicialização da aplicação"""

    pass


class ConsoleError(PepperError):
    """Erro base para operações de console"""

    pass
