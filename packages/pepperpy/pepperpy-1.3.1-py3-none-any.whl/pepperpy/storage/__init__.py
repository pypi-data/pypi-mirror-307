"""
Storage module for file and media management
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pepperpy.core.types import PathLike

from .module import StorageConfig, StorageModule

__all__ = [
    "StorageModule",
    "StorageConfig",
    "init_storage",
    "save_file",
    "read_file",
    "delete_file",
    "process_image",
    "process_document",
    "get_metadata",
]

# Global module instance
_module: Optional[StorageModule] = None


async def init_storage(config: Optional[StorageConfig] = None) -> StorageModule:
    """Initialize storage module with optional configuration"""
    global _module
    if _module is None:
        _module = StorageModule(config)
        await _module.initialize()
    return _module


async def save_file(
    source: Union[PathLike, bytes],
    destination: PathLike,
    process: bool = True,
    metadata: Optional[Dict[str, Any]] = None,
) -> Path:
    """
    Save file to storage with optional processing and metadata

    Args:
        source: Source file path or bytes content
        destination: Destination path
        process: Whether to process the file based on type
        metadata: Optional metadata to store with the file

    Returns:
        Path to saved file
    """
    if _module is None:
        raise RuntimeError("Storage module not initialized")
    return await _module.save(source, destination, process, metadata)


async def read_file(path: PathLike, as_bytes: bool = False) -> Union[str, bytes, Dict[str, Any]]:
    """
    Read file content using appropriate handler

    Args:
        path: File path
        as_bytes: Whether to return raw bytes

    Returns:
        File content in appropriate format
    """
    if _module is None:
        raise RuntimeError("Storage module not initialized")
    return await _module.read(path, as_bytes)


async def process_image(
    source: PathLike, operations: List[Dict[str, Any]] = None, output_format: str = None
) -> Path:
    """
    Process image with operations

    Args:
        source: Source image path
        operations: List of operations to apply
        output_format: Optional output format

    Returns:
        Path to processed image
    """
    if _module is None:
        raise RuntimeError("Storage module not initialized")
    return await _module.process_image(source, operations, output_format)


async def process_document(
    source: PathLike, operations: List[Dict[str, Any]] = None, output_format: str = None
) -> Path:
    """
    Process document with operations

    Args:
        source: Source document path
        operations: List of operations to apply
        output_format: Optional output format

    Returns:
        Path to processed document
    """
    if _module is None:
        raise RuntimeError("Storage module not initialized")
    return await _module.process_document(source, operations, output_format)


async def get_metadata(path: PathLike) -> Dict[str, Any]:
    """
    Get file metadata

    Args:
        path: File path

    Returns:
        File metadata
    """
    if _module is None:
        raise RuntimeError("Storage module not initialized")
    return await _module.get_metadata(path)
