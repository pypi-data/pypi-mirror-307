import mmap
import os
import queue
import threading
from dataclasses import dataclass
from typing import Any, Dict, Iterator

import torch
from torch.utils.data import DataLoader, Dataset, IterableDataset


@dataclass
class DataConfig:
    """Configuration for optimized data loading"""

    batch_size: int = 32
    num_workers: int = 4
    prefetch_factor: int = 2
    pin_memory: bool = True
    memory_map: bool = True


class MemoryMappedDataset(IterableDataset):
    """Memory-efficient dataset using memory mapping"""

    def __init__(self, data_path: str, tokenizer: Any, max_length: int = 512, stride: int = 128):
        self.data_path = data_path
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.stride = stride

        # Memory map the file
        self.file_size = os.path.getsize(data_path)
        self.file = open(data_path, "rb")
        self.mmap = mmap.mmap(self.file.fileno(), 0, access=mmap.ACCESS_READ)

    def __iter__(self) -> Iterator[Dict[str, torch.Tensor]]:
        worker_info = torch.utils.data.get_worker_info()

        if worker_info is None:
            # Single worker - process entire file
            start, end = 0, self.file_size
        else:
            # Multiple workers - split file
            per_worker = int(self.file_size / worker_info.num_workers)
            worker_id = worker_info.id
            start = worker_id * per_worker
            end = start + per_worker if worker_id < worker_info.num_workers - 1 else self.file_size

        # Seek to start position
        self.mmap.seek(start)

        # Process chunks
        current_pos = start

        while current_pos < end:
            # Read chunk
            chunk = self.mmap.read(self.max_length).decode("utf-8")
            current_pos = self.mmap.tell()

            # Tokenize
            encodings = self.tokenizer(
                chunk,
                max_length=self.max_length,
                truncation=True,
                stride=self.stride,
                return_overflowing_tokens=True,
                padding="max_length",
                return_tensors="pt",
            )

            # Yield samples
            for i in range(len(encodings["input_ids"])):
                yield {
                    "input_ids": encodings["input_ids"][i],
                    "attention_mask": encodings["attention_mask"][i],
                }

    def __del__(self):
        """Cleanup resources"""
        self.mmap.close()
        self.file.close()


class PrefetchLoader:
    """Optimized data loader with prefetching"""

    def __init__(self, loader: DataLoader, device: torch.device, prefetch_factor: int = 2):
        self.loader = loader
        self.device = device
        self.prefetch_factor = prefetch_factor

        self.queue = queue.Queue(maxsize=prefetch_factor)
        self.stop_event = threading.Event()
        self.prefetch_thread = threading.Thread(target=self._prefetch_loop, daemon=True)
        self.prefetch_thread.start()

    def _prefetch_loop(self):
        """Prefetch data in background"""
        try:
            for batch in self.loader:
                if self.stop_event.is_set():
                    break

                # Move batch to device
                device_batch = {
                    k: v.to(self.device, non_blocking=True) if isinstance(v, torch.Tensor) else v
                    for k, v in batch.items()
                }

                self.queue.put(device_batch)

        except Exception as e:
            self.queue.put(e)

        finally:
            self.queue.put(None)

    def __iter__(self):
        return self

    def __next__(self):
        batch = self.queue.get()
        if batch is None:
            raise StopIteration
        if isinstance(batch, Exception):
            raise batch
        return batch

    def __del__(self):
        self.stop_event.set()
        self.prefetch_thread.join()


def create_optimized_loader(
    dataset: Dataset, config: DataConfig, device: torch.device
) -> PrefetchLoader:
    """Create optimized data loader"""
    loader = DataLoader(
        dataset,
        batch_size=config.batch_size,
        num_workers=config.num_workers,
        pin_memory=config.pin_memory,
    )

    return PrefetchLoader(loader, device, prefetch_factor=config.prefetch_factor)
