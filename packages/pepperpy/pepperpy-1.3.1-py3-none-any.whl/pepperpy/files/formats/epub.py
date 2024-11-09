"""EPUB file format handling"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ebooklib import epub

from pepperpy.core.types import PathLike
from pepperpy.storage.exceptions import ProcessingError, StorageError


class EPUBMetadata(Dict[str, Any]):
    """EPUB metadata container"""

    pass


class EPUBProcessor:
    """EPUB file processing"""

    async def create_epub(
        self,
        title: str,
        authors: List[str],
        chapters: List[Tuple[str, str]],  # (title, content)
        metadata: Optional[EPUBMetadata] = None,
        output: Optional[PathLike] = None,
    ) -> Path:
        """Create EPUB file"""
        try:
            book = epub.EpubBook()
            book.set_title(title)
            for author in authors:
                book.add_author(author)

            if metadata:
                for key, value in metadata.items():
                    book.add_metadata("DC", key, value)

            chapters_list = []
            for i, (chapter_title, content) in enumerate(chapters, 1):
                chapter = epub.EpubHtml(
                    title=chapter_title, file_name=f"chapter_{i}.xhtml", content=content
                )
                book.add_item(chapter)
                chapters_list.append(chapter)

            book.toc = chapters_list
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())
            book.spine = chapters_list

            output_path = Path(output or f"{title}.epub")
            epub.write_epub(str(output_path), book)
            return output_path

        except Exception as e:
            raise ProcessingError(f"EPUB creation failed: {e}") from e

    async def get_metadata(self, path: PathLike) -> Dict[str, Any]:
        """Get EPUB metadata"""
        try:
            book = epub.read_epub(str(path))
            return {
                "title": book.get_metadata("DC", "title"),
                "authors": book.get_metadata("DC", "creator"),
                "language": book.get_metadata("DC", "language"),
                "identifier": book.get_metadata("DC", "identifier"),
                "description": book.get_metadata("DC", "description"),
                "publisher": book.get_metadata("DC", "publisher"),
                "date": book.get_metadata("DC", "date"),
            }
        except Exception as e:
            raise StorageError(f"Failed to get EPUB metadata: {e}") from e
