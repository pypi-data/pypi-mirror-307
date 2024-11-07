from dataclasses import dataclass
from typing import Optional

import torch
import torch.nn.functional as F


@dataclass
class PageConfig:
    """Configuration for paged attention"""

    page_size: int = 16  # Size of each memory page
    n_pages: int = 1024  # Number of pages to maintain
    block_size: int = 64  # Block size for computation


class PagedAttention:
    """Memory-efficient paged attention implementation"""

    def __init__(self, config: PageConfig):
        self.config = config
        self.pages = {}
        self.page_table = {}

    def forward(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        mask: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """Forward pass with paged attention"""
        batch_size, n_heads, seq_len, d_head = query.shape

        # Split sequences into pages
        n_pages = (seq_len + self.config.page_size - 1) // self.config.page_size

        # Reshape inputs into pages
        key_pages = key.view(batch_size, n_heads, n_pages, self.config.page_size, d_head)
        value_pages = value.view(batch_size, n_heads, n_pages, self.config.page_size, d_head)

        # Process attention in blocks
        output = torch.zeros_like(query)
        for i in range(0, seq_len, self.config.block_size):
            block_end = min(i + self.config.block_size, seq_len)
            q_block = query[:, :, i:block_end]

            # Calculate attention scores for block
            scores = torch.matmul(q_block, key_pages.transpose(-2, -1))
            if mask is not None:
                scores = scores + mask[:, :, i:block_end].unsqueeze(-1)

            # Apply softmax and compute weighted sum
            attn_probs = F.softmax(scores, dim=-1)
            block_output = torch.matmul(attn_probs, value_pages)

            output[:, :, i:block_end] = block_output.view(
                batch_size, n_heads, block_end - i, d_head
            )

        return output

    def allocate_page(self, key: str, size: int) -> None:
        """Allocate new memory page"""
        if len(self.pages) >= self.config.n_pages:
            self._evict_pages()

        page_id = len(self.pages)
        self.pages[page_id] = torch.zeros(size)
        self.page_table[key] = page_id

    def _evict_pages(self) -> None:
        """Evict least recently used pages"""
        # Simple LRU eviction
        n_evict = len(self.pages) // 4  # Evict 25% of pages
        sorted_pages = sorted(self.page_table.items(), key=lambda x: x[1])

        for key, _ in sorted_pages[:n_evict]:
            page_id = self.page_table[key]
            del self.pages[page_id]
            del self.page_table[key]
