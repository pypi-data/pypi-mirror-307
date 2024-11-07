from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class MoEConfig:
    """Configuration for Mixture of Experts"""

    num_experts: int = 8
    expert_size: int = 1024
    k: int = 2  # Number of experts to route to
    capacity_factor: float = 1.25
    eval_capacity_factor: float = 2.0
    min_expert_capacity: int = 4


class ExpertLayer(nn.Module):
    """Single expert implementation"""

    def __init__(self, input_size: int, expert_size: int):
        super().__init__()
        self.w1 = nn.Linear(input_size, expert_size)
        self.w2 = nn.Linear(expert_size, input_size)
        self.activation = nn.GELU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.w1(x)
        x = self.activation(x)
        x = self.w2(x)
        return x


class MoELayer(nn.Module):
    """Mixture of Experts layer with efficient routing"""

    def __init__(self, config: MoEConfig, input_size: int):
        super().__init__()
        self.config = config

        # Create experts
        self.experts = nn.ModuleList(
            [ExpertLayer(input_size, config.expert_size) for _ in range(config.num_experts)]
        )

        # Router
        self.router = nn.Linear(input_size, config.num_experts)
        self.softplus = nn.Softplus()

    def forward(self, inputs: torch.Tensor, is_training: bool = True) -> torch.Tensor:
        """Forward pass with efficient routing"""
        batch_size, seq_len, d_model = inputs.shape

        # Get router scores
        router_logits = self.router(inputs)
        router_probs = F.softmax(router_logits, dim=-1)

        # Select top-k experts
        k = self.config.k
        top_k_probs, top_k_indices = torch.topk(router_probs, k, dim=-1)
        top_k_probs = top_k_probs / top_k_probs.sum(dim=-1, keepdim=True)

        # Calculate expert capacity
        capacity_factor = (
            self.config.capacity_factor if is_training else self.config.eval_capacity_factor
        )
        expert_capacity = max(
            int((batch_size * seq_len * capacity_factor) / self.config.num_experts),
            self.config.min_expert_capacity,
        )

        # Create dispatch tensors
        expert_mask = torch.zeros(
            (batch_size * seq_len, self.config.num_experts), device=inputs.device
        )
        flat_indices = (
            torch.arange(batch_size * seq_len, device=inputs.device).unsqueeze(1).expand(-1, k)
        )
        expert_mask[flat_indices, top_k_indices.view(-1, k)] = top_k_probs.view(-1, k)

        # Limit tokens per expert using capacity
        expert_mask = expert_mask.scatter_add_(
            0, top_k_indices.view(-1, k), top_k_probs.view(-1, k)
        ).clamp_(max=expert_capacity)

        # Reshape inputs for expert computation
        flat_inputs = inputs.view(-1, d_model)
        expert_inputs = torch.einsum("be,ed->bed", expert_mask, flat_inputs)

        # Process with experts
        expert_outputs = []
        for i, expert in enumerate(self.experts):
            expert_output = expert(expert_inputs[:, i])
            expert_outputs.append(expert_output)

        # Combine expert outputs
        combined_outputs = torch.stack(expert_outputs, dim=1)
        final_output = torch.einsum("be,bed->ed", expert_mask, combined_outputs)

        return final_output.view(batch_size, seq_len, d_model)


class MoEOptimizer:
    """Optimizer for Mixture of Experts models"""

    @staticmethod
    def convert_to_moe(model: nn.Module, config: MoEConfig) -> nn.Module:
        """Convert transformer layers to MoE"""
        for name, module in model.named_children():
            if isinstance(module, nn.Linear) and module.in_features == module.out_features:
                # Replace feed-forward layers with MoE
                setattr(model, name, MoELayer(config, module.in_features))
            elif len(list(module.children())) > 0:
                # Recurse for nested modules
                MoEOptimizer.convert_to_moe(module, config)

        return model
