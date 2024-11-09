from pepperpy.core.exceptions import PepperPyError


class AIError(PepperPyError):
    """Base exception for AI module"""

    pass


class ModelNotFoundError(AIError):
    """Raised when AI model is not found"""

    pass


class ProviderError(AIError):
    """Raised when there's an error with the AI provider"""

    pass


class InitializationError(AIError):
    """Raised when module initialization fails"""

    pass


class ConfigurationError(AIError):
    """Raised when there's an error in the configuration"""

    pass
