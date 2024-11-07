from dataclasses import dataclass
from typing import Dict

import torch
import torch.nn as nn
import wandb
from torch.cuda.amp import GradScaler, autocast


@dataclass
class TrainingConfig:
    """Configuration for efficient training"""

    gradient_accumulation_steps: int = 4
    mixed_precision: bool = True
    gradient_checkpointing: bool = True
    max_grad_norm: float = 1.0
    warmup_steps: int = 100
    log_interval: int = 10


class MemoryEfficientTrainer:
    """Memory-efficient model training"""

    def __init__(self, model: nn.Module, optimizer: torch.optim.Optimizer, config: TrainingConfig):
        self.model = model
        self.optimizer = optimizer
        self.config = config
        self.scaler = GradScaler() if config.mixed_precision else None

        # Enable gradient checkpointing if requested
        if config.gradient_checkpointing:
            self.model.gradient_checkpointing_enable()

        # Initialize tracking
        self.step = 0
        self.epoch = 0
        self.best_loss = float("inf")

        # Setup wandb logging
        wandb.init(project="model_training")

    def _get_lr_scale(self) -> float:
        """Get learning rate scale based on warmup"""
        if self.step < self.config.warmup_steps:
            return float(self.step) / float(max(1, self.config.warmup_steps))
        return 1.0

    async def train_step(
        self, batch: Dict[str, torch.Tensor], labels: torch.Tensor
    ) -> Dict[str, float]:
        """Single training step with optimizations"""
        # Accumulate gradients
        self.model.train()
        total_loss = 0

        for micro_step in range(self.config.gradient_accumulation_steps):
            # Get batch slice
            batch_slice = {
                k: v[micro_step :: self.config.gradient_accumulation_steps]
                for k, v in batch.items()
            }
            labels_slice = labels[micro_step :: self.config.gradient_accumulation_steps]

            # Forward pass with mixed precision
            with autocast(enabled=self.config.mixed_precision):
                outputs = self.model(**batch_slice, labels=labels_slice)
                loss = outputs.loss / self.config.gradient_accumulation_steps

            # Backward pass with gradient scaling
            if self.scaler is not None:
                self.scaler.scale(loss).backward()
            else:
                loss.backward()

            total_loss += loss.item()

        # Optimize step
        if self.scaler is not None:
            self.scaler.unscale_(self.optimizer)
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.config.max_grad_norm)
            self.scaler.step(self.optimizer)
            self.scaler.update()
        else:
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.config.max_grad_norm)
            self.optimizer.step()

        self.optimizer.zero_grad()

        # Update learning rate
        lr_scale = self._get_lr_scale()
        for param_group in self.optimizer.param_groups:
            param_group["lr"] = lr_scale * param_group["initial_lr"]

        # Log metrics
        metrics = {
            "loss": total_loss,
            "learning_rate": lr_scale * self.optimizer.param_groups[0]["initial_lr"],
            "step": self.step,
            "epoch": self.epoch,
        }

        if self.step % self.config.log_interval == 0:
            wandb.log(metrics)

        self.step += 1
        return metrics

    async def save_checkpoint(self, path: str, loss: float) -> None:
        """Save optimized checkpoint"""
        if loss < self.best_loss:
            self.best_loss = loss
            checkpoint = {
                "model_state": self.model.state_dict(),
                "optimizer_state": self.optimizer.state_dict(),
                "scaler_state": self.scaler.state_dict() if self.scaler else None,
                "step": self.step,
                "epoch": self.epoch,
                "best_loss": self.best_loss,
                "config": self.config,
            }
            torch.save(checkpoint, path)

    @classmethod
    async def load_checkpoint(
        cls, path: str, model: nn.Module, optimizer: torch.optim.Optimizer
    ) -> "MemoryEfficientTrainer":
        """Load checkpoint and resume training"""
        checkpoint = torch.load(path)

        trainer = cls(model=model, optimizer=optimizer, config=checkpoint["config"])

        trainer.model.load_state_dict(checkpoint["model_state"])
        trainer.optimizer.load_state_dict(checkpoint["optimizer_state"])
        if trainer.scaler and checkpoint["scaler_state"]:
            trainer.scaler.load_state_dict(checkpoint["scaler_state"])

        trainer.step = checkpoint["step"]
        trainer.epoch = checkpoint["epoch"]
        trainer.best_loss = checkpoint["best_loss"]

        return trainer
