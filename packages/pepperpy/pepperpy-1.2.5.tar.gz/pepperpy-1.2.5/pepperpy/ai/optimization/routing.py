from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class RoutingConfig:
    """Configuration for Routing Transformer"""

    num_experts: int = 8
    expert_size: int = 1024
    num_clusters: int = 4
    clustering_algorithm: str = "kmeans"  # or "online"
    routing_strategy: str = "gaussian"  # or "cosine"
    temperature: float = 0.1
    capacity_factor: float = 1.25


class RoutingExpert(nn.Module):
    """Expert with clustering-based routing"""

    def __init__(self, config: RoutingConfig, input_size: int):
        super().__init__()
        self.config = config

        # Expert network
        self.expert = nn.Sequential(
            nn.Linear(input_size, config.expert_size),
            nn.GELU(),
            nn.Linear(config.expert_size, input_size),
        )

        # Clustering parameters
        self.centroids = nn.Parameter(torch.randn(config.num_clusters, input_size))

        # Optional online clustering
        if config.clustering_algorithm == "online":
            self.register_buffer("cluster_counts", torch.zeros(config.num_clusters))
            self.register_buffer("cluster_sum", torch.zeros(config.num_clusters, input_size))

    def update_clusters(self, inputs: torch.Tensor) -> None:
        """Update cluster centroids with online algorithm"""
        if self.config.clustering_algorithm != "online":
            return

        # Calculate distances to centroids
        distances = torch.cdist(inputs, self.centroids)
        assignments = torch.argmin(distances, dim=1)

        # Update cluster statistics
        for i in range(self.config.num_clusters):
            mask = assignments == i
            if not mask.any():
                continue

            cluster_inputs = inputs[mask]
            self.cluster_counts[i] += len(cluster_inputs)
            self.cluster_sum[i] += cluster_inputs.sum(dim=0)

            # Update centroid
            self.centroids.data[i] = self.cluster_sum[i] / self.cluster_counts[i]

    def route(self, inputs: torch.Tensor) -> torch.Tensor:
        """Calculate routing probabilities"""
        if self.config.routing_strategy == "gaussian":
            # Gaussian kernel routing
            distances = torch.cdist(inputs, self.centroids)
            scores = -distances / self.config.temperature
        else:
            # Cosine similarity routing
            inputs_norm = F.normalize(inputs, dim=-1)
            centroids_norm = F.normalize(self.centroids, dim=-1)
            scores = torch.matmul(inputs_norm, centroids_norm.t())
            scores = scores / self.config.temperature

        return F.softmax(scores, dim=-1)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        """Forward pass with routing"""
        # Get routing probabilities
        routing_probs = self.route(inputs)

        # Process with expert
        expert_outputs = self.expert(inputs)

        # Weight outputs by routing probabilities
        weighted_outputs = torch.einsum("be,bd->bd", routing_probs, expert_outputs)

        return weighted_outputs


class RoutingTransformer(nn.Module):
    """Transformer with clustered routing"""

    def __init__(self, config: RoutingConfig, input_size: int):
        super().__init__()
        self.config = config

        # Create experts
        self.experts = nn.ModuleList(
            [RoutingExpert(config, input_size) for _ in range(config.num_experts)]
        )

        # Output projection
        self.output_proj = nn.Linear(input_size, input_size)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        """Forward pass with routed experts"""
        batch_size, seq_len, dim = inputs.shape

        # Process with experts
        expert_outputs = []
        for expert in self.experts:
            # Update clusters if using online algorithm
            if self.config.clustering_algorithm == "online":
                expert.update_clusters(inputs.view(-1, dim))

            # Get expert output
            expert_output = expert(inputs.view(-1, dim))
            expert_outputs.append(expert_output)

        # Combine expert outputs
        combined_output = torch.stack(expert_outputs, dim=1)
        final_output = combined_output.mean(dim=1)

        # Project output
        return self.output_proj(final_output).view(batch_size, seq_len, dim)
