"""Document processing implementation"""

from pathlib import Path
from typing import Any, Dict, List

import fitz  # PyMuPDF

from pepperpy.core.exceptions import StorageError
from pepperpy.core.types import PathLike

from .base import BaseProcessor


class DocumentProcessor(BaseProcessor):
    """Document processing with PyMuPDF"""

    SUPPORTED_FORMATS = ["pdf", "docx", "doc", "odt", "epub"]

    async def process(self, source: PathLike, operations: List[Dict[str, Any]]) -> None:
        """Process document with operations"""
        try:
            doc = await self._load_document(source)

            if operations:
                for op in operations:
                    await self._apply_operation(doc, op)

            return await self._save_document(doc, source, Path(source).suffix[1:])
        except Exception as e:
            raise StorageError(f"Document processing failed: {e}") from e

    async def get_metadata(self, path: PathLike) -> Dict[str, Any]:
        """Get document metadata"""
        try:
            doc = fitz.open(path)
            return {
                "format": doc.name,
                "pages": len(doc),
                "title": doc.metadata.get("title"),
                "author": doc.metadata.get("author"),
                "creation_date": doc.metadata.get("creationDate"),
                "modification_date": doc.metadata.get("modDate"),
            }
        except Exception as e:
            raise StorageError(f"Failed to get document metadata: {e}") from e
