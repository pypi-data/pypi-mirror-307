import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Protocol


@dataclass
class TextChunk:
    """Represents a chunk of text"""

    content: str
    index: int
    metadata: dict = field(default_factory=dict)
    token_count: Optional[int] = None


class ChunkingStrategy(ABC):
    """Base class for text chunking strategies"""

    @abstractmethod
    def split(self, text: str, max_chunk_size: int) -> List[TextChunk]:
        """Split text into chunks"""
        pass


class SmartChunker(ChunkingStrategy):
    """Intelligent text chunking with overlap"""

    def __init__(self, overlap: int = 100):
        self.overlap = overlap
        self._splitter = re.compile(r"(?<=[.!?])\s+")

    def split(self, text: str, max_chunk_size: int = 1000) -> List[TextChunk]:
        # First split into sentences
        sentences = [s.strip() for s in self._splitter.split(text) if s.strip()]

        chunks = []
        current_chunk = []
        current_size = 0

        for sentence in sentences:
            sentence_size = len(sentence)

            # If adding this sentence exceeds the limit
            if current_size + sentence_size > max_chunk_size and current_chunk:
                # Create chunk with metadata
                chunk_text = " ".join(current_chunk)
                chunks.append(
                    TextChunk(
                        content=chunk_text,
                        index=len(chunks),
                        metadata={
                            "start_sentence": current_chunk[0][:50],
                            "end_sentence": current_chunk[-1][:50],
                            "sentences": len(current_chunk),
                        },
                    )
                )

                # Keep overlap for context
                overlap_text = current_chunk[-1] if self.overlap > 0 else ""
                current_chunk = [overlap_text] if overlap_text else []
                current_size = len(overlap_text) if overlap_text else 0

            current_chunk.append(sentence)
            current_size += sentence_size

        # Add remaining chunk
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append(
                TextChunk(
                    content=chunk_text,
                    index=len(chunks),
                    metadata={
                        "start_sentence": current_chunk[0][:50],
                        "end_sentence": current_chunk[-1][:50],
                        "sentences": len(current_chunk),
                    },
                )
            )

        return chunks


class MarkdownChunker(ChunkingStrategy):
    """Chunk text by markdown sections"""

    def split(self, text: str, max_chunk_size: int = 1000) -> List[TextChunk]:
        # Split by markdown headers
        sections = re.split(r"^#{1,6}\s+", text, flags=re.MULTILINE)
        chunks = []

        for i, section in enumerate(sections):
            if not section.strip():
                continue

            # If section is too large, use smart chunking
            if len(section) > max_chunk_size:
                sub_chunker = SmartChunker()
                sub_chunks = sub_chunker.split(section, max_chunk_size)
                for chunk in sub_chunks:
                    chunk.metadata["section"] = i
                chunks.extend(sub_chunks)
            else:
                chunks.append(
                    TextChunk(
                        content=section.strip(),
                        index=len(chunks),
                        metadata={"section": i},
                    )
                )

        return chunks


class TokenCounter(Protocol):
    """Protocol for token counting"""

    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        pass
