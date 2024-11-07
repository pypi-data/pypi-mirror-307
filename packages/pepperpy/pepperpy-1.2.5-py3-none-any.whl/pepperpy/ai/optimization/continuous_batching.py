import asyncio
from dataclasses import dataclass

import torch


@dataclass
class BatchConfig:
    """Configuration for continuous batching"""

    max_batch_size: int = 32
    max_sequence_length: int = 2048
    prefetch_size: int = 2
    kv_cache_size: int = 1024 * 1024  # 1M tokens


class ContinuousBatchProcessor:
    """Efficient continuous batching with KV cache"""

    def __init__(self, config: BatchConfig):
        self.config = config
        self.kv_cache = {}
        self.request_queue = asyncio.Queue()
        self.current_batch = []

    async def add_request(
        self, input_ids: torch.Tensor, attention_mask: torch.Tensor, request_id: str
    ) -> None:
        """Add request to processing queue"""
        await self.request_queue.put((request_id, input_ids, attention_mask))

        if len(self.current_batch) >= self.config.max_batch_size:
            await self._process_batch()

    async def _process_batch(self) -> None:
        """Process current batch efficiently"""
        if not self.current_batch:
            return

        # Combine requests into single batch
        batch_ids = []
        batch_masks = []
        batch_positions = []
        current_pos = 0

        for req_id, ids, mask in self.current_batch:
            # Check KV cache
            if req_id in self.kv_cache:
                cached_length = self.kv_cache[req_id]["length"]
                # Use cached KV, only process new tokens
                ids = ids[:, cached_length:]
                mask = mask[:, cached_length:]
                batch_positions.append(cached_length)
            else:
                batch_positions.append(0)

            batch_ids.append(ids)
            batch_masks.append(mask)
            current_pos += ids.size(1)

        # Pad sequences
        max_len = max(ids.size(1) for ids in batch_ids)
        padded_ids = []
        padded_masks = []

        for ids, mask in zip(batch_ids, batch_masks):
            pad_len = max_len - ids.size(1)
            padded_ids.append(torch.nn.functional.pad(ids, (0, pad_len)))
            padded_masks.append(torch.nn.functional.pad(mask, (0, pad_len)))

        # Create batch tensors
        batch_input_ids = torch.cat(padded_ids, dim=0)
        batch_attention_mask = torch.cat(padded_masks, dim=0)

        # Process batch through model
        await self._forward_batch(batch_input_ids, batch_attention_mask)

        # Prune KV cache if needed
        if len(self.kv_cache) * current_pos > self.config.kv_cache_size:
            self._prune_kv_cache()

    def _prune_kv_cache(self) -> None:
        """Remove oldest entries from KV cache"""
        sorted_entries = sorted(self.kv_cache.items(), key=lambda x: x[1]["position"])

        # Remove oldest entries until under limit
        while len(self.kv_cache) * sorted_entries[-1][1]["length"] > self.config.kv_cache_size:
            req_id, _ = sorted_entries.pop(0)
            del self.kv_cache[req_id]
