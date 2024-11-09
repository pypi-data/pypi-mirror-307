"""Video file format handling"""

from typing import Any, Dict, Optional

import av

from pepperpy.core.types import PathLike
from pepperpy.storage.exceptions import ProcessingError, StorageError


class VideoProcessor:
    """Video file processing"""

    SUPPORTED_FORMATS = ["mp4", "avi", "mkv", "mov", "webm"]

    async def convert_format(
        self,
        source: PathLike,
        destination: PathLike,
        format: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Convert video format"""
        try:
            input_container = av.open(str(source))
            output_container = av.open(str(destination), mode="w")

            # Copy stream parameters
            stream_options = {}
            if options:
                stream_options.update(options)

            # Setup streams
            for stream in input_container.streams:
                if stream.type in ("video", "audio"):
                    output_container.add_stream(template=stream, **stream_options)

            # Process frames
            for packet in input_container.demux():
                if packet.dts is None:
                    continue
                try:
                    packet.decode()
                    output_container.mux(packet)
                except av.AVError:
                    continue

            # Close containers
            input_container.close()
            output_container.close()

        except Exception as e:
            raise ProcessingError(f"Video conversion failed: {e}") from e

    async def get_metadata(self, path: PathLike) -> Dict[str, Any]:
        """Get video metadata"""
        try:
            with av.open(str(path)) as container:
                video_stream = next(s for s in container.streams if s.type == "video")
                return {
                    "format": container.format.name,
                    "duration": float(container.duration) / av.time_base,
                    "width": video_stream.width,
                    "height": video_stream.height,
                    "fps": float(video_stream.average_rate),
                    "codec": video_stream.codec_context.name,
                }
        except Exception as e:
            raise StorageError(f"Failed to get video metadata: {e}") from e

    def is_supported(self, path: PathLike) -> bool:
        """Check if file is supported video format"""
        try:
            with av.open(str(path)) as container:
                return any(s.type == "video" for s in container.streams)
        except Exception:
            return False
