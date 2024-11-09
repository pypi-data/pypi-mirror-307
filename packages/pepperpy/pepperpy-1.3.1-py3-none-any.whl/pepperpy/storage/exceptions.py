"""Storage-specific exceptions"""

from pepperpy.core.exceptions import PepperPyError


class StorageError(PepperPyError):
    """Base exception for storage errors"""

    pass


class ProcessingError(StorageError):
    """Error during file processing"""

    pass


class ValidationError(StorageError):
    """Error during file validation"""

    pass


class FileNotFoundError(StorageError):
    """File not found error"""

    pass


class FileTypeError(StorageError):
    """Invalid file type error"""

    pass


class FileSizeError(StorageError):
    """File size limit exceeded"""

    pass
