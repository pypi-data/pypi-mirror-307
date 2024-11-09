"""Audio file format handling"""

from typing import Any, Dict, Optional

import mutagen
import soundfile as sf

from pepperpy.core.types import PathLike
from pepperpy.storage.exceptions import ProcessingError, StorageError


class AudioProcessor:
    """Audio file processing"""

    SUPPORTED_FORMATS = ["wav", "mp3", "ogg", "flac", "m4a", "aac"]

    async def convert_format(
        self,
        source: PathLike,
        destination: PathLike,
        format: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Convert audio format."""
        try:
            data, samplerate = sf.read(str(source))
            sf.write(str(destination), data, samplerate, format=format, **(options or {}))
        except Exception as e:
            raise ProcessingError(f"Audio conversion failed: {e}") from e

    async def get_metadata(self, path: PathLike) -> Dict[str, Any]:
        """Get audio metadata"""
        try:
            audio = mutagen.File(str(path))
            if not audio:
                raise StorageError("Could not read audio metadata")

            return {
                "format": audio.mime[0].split("/")[-1],
                "duration": audio.info.length,
                "bitrate": getattr(audio.info, "bitrate", None),
                "channels": getattr(audio.info, "channels", None),
                "sample_rate": getattr(audio.info, "sample_rate", None),
                "tags": dict(audio.tags or {}),
            }
        except Exception as e:
            raise StorageError(f"Failed to get audio metadata: {e}") from e

    def is_supported(self, path: PathLike) -> bool:
        """Check if file is supported audio format"""
        try:
            audio = mutagen.File(str(path))
            return audio is not None
        except Exception:
            return False
