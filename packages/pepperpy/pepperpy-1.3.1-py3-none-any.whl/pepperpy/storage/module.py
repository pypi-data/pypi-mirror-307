"""Enhanced storage system with support for files and media"""

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Union

import aiofiles

from pepperpy.core import BaseModule, ModuleConfig
from pepperpy.core.exceptions import StorageError
from pepperpy.core.types import JsonDict, PathLike


@dataclass
class StorageConfig(ModuleConfig):
    """Storage configuration"""

    base_path: PathLike = "./storage"
    temp_path: PathLike = "/tmp/pepperpy/storage"
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    supported_formats: Dict[str, List[str]] = None
    image_quality: int = 85
    preserve_metadata: bool = True
    auto_orient: bool = True
    chunk_size: int = 8192  # 8KB for streaming

    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = {
                "document": ["txt", "pdf", "doc", "docx", "xls", "xlsx"],
                "image": ["jpg", "jpeg", "png", "gif", "webp", "svg"],
                "audio": ["mp3", "wav", "ogg", "flac"],
                "video": ["mp4", "webm", "avi", "mov"],
                "data": ["json", "yaml", "yml", "xml", "csv"],
            }


class StorageModule(BaseModule):
    """Unified storage system for files and media"""

    __module_name__ = "storage"
    __dependencies__ = ["cache"]

    def __init__(self, config: Optional[StorageConfig] = None):
        super().__init__(config or StorageConfig())
        self._processors = {}
        self._handlers = {}
        self._base_path = Path(self.config.base_path)
        self._temp_path = Path(self.config.temp_path)
        self._lock = asyncio.Lock()

    async def initialize(self) -> None:
        """Initialize storage system"""
        await super().initialize()
        self._base_path.mkdir(parents=True, exist_ok=True)
        self._temp_path.mkdir(parents=True, exist_ok=True)
        await self._setup_processors()
        await self._setup_handlers()

    async def cleanup(self) -> None:
        """Cleanup storage system"""
        # Cleanup temporary files
        if self._temp_path.exists():
            for file in self._temp_path.glob("*"):
                try:
                    file.unlink()
                except Exception as e:
                    self._logger.warning(f"Failed to remove temp file {file}: {e}")
        await super().cleanup()

    async def save(
        self, source: Union[PathLike, bytes], destination: PathLike, process: bool = True
    ) -> Path:
        """Save file to storage with optional processing"""
        try:
            dest_path = Path(destination)
            file_type = self._get_file_type(dest_path)

            if process and file_type in self._processors:
                processor = self._processors[file_type]
                return await processor.process(source, destination)

            # Direct file save if no processing needed
            if isinstance(source, (str, Path)):
                return await self._copy_file(Path(source), dest_path)
            return await self._save_bytes(source, dest_path)
        except Exception as e:
            raise StorageError(f"Failed to save file: {e}") from e

    async def read(self, path: PathLike, as_bytes: bool = False) -> Union[str, bytes, JsonDict]:
        """Read file content using appropriate handler"""
        try:
            file_path = Path(path)
            if not file_path.exists():
                raise StorageError(f"File not found: {path}")

            handler = self._get_handler(file_path)
            if handler and not as_bytes:
                return await handler.read(file_path)

            return await self._read_bytes(file_path)
        except Exception as e:
            raise StorageError(f"Failed to read file: {e}") from e

    async def delete(self, path: PathLike) -> None:
        """Delete file from storage"""
        try:
            file_path = Path(path)
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            raise StorageError(f"Failed to delete file: {e}") from e

    async def exists(self, path: PathLike) -> bool:
        """Check if file exists"""
        return Path(path).exists()

    def _get_file_type(self, path: Path) -> str:
        """Determine file type from extension"""
        ext = path.suffix.lower()[1:]  # Remove dot
        for type_, extensions in self.config.supported_formats.items():
            if ext in extensions:
                return type_
        return "unknown"

    async def _copy_file(self, source: Path, dest: Path) -> Path:
        """Copy file with chunked reading"""
        dest.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(source, "rb") as src:
            async with aiofiles.open(dest, "wb") as dst:
                while chunk := await src.read(self.config.chunk_size):
                    await dst.write(chunk)

        return dest

    async def _save_bytes(self, data: bytes, dest: Path) -> Path:
        """Save bytes to file"""
        dest.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(dest, "wb") as f:
            await f.write(data)

        return dest

    async def _read_bytes(self, path: Path) -> bytes:
        """Read file as bytes"""
        async with aiofiles.open(path, "rb") as f:
            return await f.read()
