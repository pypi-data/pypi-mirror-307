from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np
import plotly.graph_objects as go
from pyvis.network import Network


@dataclass
class NetworkGraphConfig:
    """Configuration for network visualizations"""

    height: str = "750px"
    width: str = "100%"
    bgcolor: str = "#ffffff"
    font_color: str = "#000000"
    directed: bool = True


class AdvancedVisualizer:
    """Advanced visualization tools for AI analysis"""

    def plot_pipeline_flow(
        self, pipeline_steps: List[Dict[str, Any]], metrics: Dict[str, Any]
    ) -> Network:
        """Create interactive pipeline flow visualization"""
        net = Network(
            height="750px",
            width="100%",
            bgcolor="#ffffff",
            font_color="black",
            directed=True,
        )

        # Add nodes for each step
        for step in pipeline_steps:
            success_rate = metrics["operations"].get(step["name"], {}).get("success_rate", 0)
            color = self._get_health_color(success_rate)

            net.add_node(
                step["name"],
                label=step["name"],
                title=f"Success Rate: {success_rate:.2%}",
                color=color,
                size=30,
            )

        # Add edges between steps
        for i in range(len(pipeline_steps) - 1):
            net.add_edge(pipeline_steps[i]["name"], pipeline_steps[i + 1]["name"])

        return net

    def plot_embedding_clusters(
        self,
        embeddings: np.ndarray,
        labels: Optional[List[str]] = None,
        n_components: int = 2,
    ) -> go.Figure:
        """Plot embedding clusters using dimensionality reduction"""
        from sklearn.manifold import TSNE

        # Reduce dimensions for visualization
        tsne = TSNE(n_components=n_components, random_state=42)
        reduced_embeddings = tsne.fit_transform(embeddings)

        if n_components == 3:
            fig = go.Figure(
                data=[
                    go.Scatter3d(
                        x=reduced_embeddings[:, 0],
                        y=reduced_embeddings[:, 1],
                        z=reduced_embeddings[:, 2],
                        mode="markers+text",
                        text=labels if labels else None,
                        hoverinfo="text",
                    )
                ]
            )

            fig.update_layout(
                scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"),
                title="Embedding Clusters (3D)",
            )
        else:
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=reduced_embeddings[:, 0],
                        y=reduced_embeddings[:, 1],
                        mode="markers+text",
                        text=labels if labels else None,
                        hoverinfo="text",
                    )
                ]
            )

            fig.update_layout(xaxis_title="X", yaxis_title="Y", title="Embedding Clusters (2D)")

        return fig

    def plot_attention_heatmap(self, attention_weights: np.ndarray, tokens: List[str]) -> go.Figure:
        """Plot attention weights heatmap"""
        fig = go.Figure(
            data=go.Heatmap(z=attention_weights, x=tokens, y=tokens, colorscale="Viridis")
        )

        fig.update_layout(
            title="Attention Weights",
            xaxis_title="Target Tokens",
            yaxis_title="Source Tokens",
        )

        return fig

    def _get_health_color(self, success_rate: float) -> str:
        """Get color based on health/success rate"""
        if success_rate >= 0.9:
            return "#00ff00"  # Green
        elif success_rate >= 0.7:
            return "#ffff00"  # Yellow
        else:
            return "#ff0000"  # Red
