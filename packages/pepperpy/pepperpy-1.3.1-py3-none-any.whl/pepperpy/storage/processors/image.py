"""Image processing implementation"""

import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional

from PIL import Image, ImageOps

from pepperpy.core.types import PathLike
from pepperpy.storage.exceptions import ProcessingError, StorageError

from .base import BaseProcessor


class ImageProcessor(BaseProcessor):
    """Image processing with Pillow"""

    SUPPORTED_FORMATS = ["jpg", "jpeg", "png", "gif", "webp", "bmp"]

    async def process(
        self,
        source: PathLike,
        operations: Optional[List[Dict[str, Any]]] = None,
        output_format: Optional[str] = None,
    ) -> Path:
        """Process image with operations"""
        try:
            image = await self._load_image(source)

            if operations:
                for op in operations:
                    image = await self._apply_operation(image, op)

            return await self._save_image(image, source, output_format or Path(source).suffix[1:])
        except Exception as e:
            raise ProcessingError(f"Image processing failed: {e}") from e

    async def get_metadata(self, path: PathLike) -> Dict[str, Any]:
        """Get image metadata"""
        try:
            with Image.open(path) as img:
                return {
                    "format": img.format,
                    "mode": img.mode,
                    "size": img.size,
                    "width": img.width,
                    "height": img.height,
                    "exif": img.getexif() if hasattr(img, "_getexif") else None,
                }
        except Exception as e:
            raise StorageError(f"Failed to get image metadata: {e}") from e

    async def _load_image(self, path: PathLike) -> Image.Image:
        """Load image file"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, Image.open, path)

    async def _save_image(self, image: Image.Image, source: PathLike, format: str) -> Path:
        """Save processed image"""
        output_path = Path(source).with_suffix(f".{format}")
        await asyncio.get_event_loop().run_in_executor(
            None,
            image.save,
            output_path,
            format.upper(),
            quality=self.config.image_quality,
            optimize=True,
        )
        return output_path

    async def _apply_operation(self, image: Image.Image, operation: Dict[str, Any]) -> Image.Image:
        """Apply single operation to image"""
        op_type = operation["type"]
        params = operation.get("params", {})

        if op_type == "resize":
            return image.resize((params["width"], params["height"]), Image.Resampling.LANCZOS)
        elif op_type == "rotate":
            return image.rotate(params["angle"], expand=params.get("expand", True))
        elif op_type == "crop":
            return image.crop((params["left"], params["top"], params["right"], params["bottom"]))
        elif op_type == "auto_orient":
            return ImageOps.exif_transpose(image)
        else:
            raise ValueError(f"Unsupported operation: {op_type}")
