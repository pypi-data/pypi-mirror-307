from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go


@dataclass
class VisualizationConfig:
    """Configuration for visualizations"""

    theme: str = "plotly"
    width: int = 800
    height: int = 500
    template: str = "plotly_white"


class AIVisualizer:
    """Visualization tools for AI metrics and analysis"""

    def __init__(self, config: Optional[VisualizationConfig] = None):
        self.config = config or VisualizationConfig()

    def plot_metrics_timeline(self, metrics: List[Dict[str, Any]]) -> go.Figure:
        """Plot metrics over time"""
        df = pd.DataFrame(metrics)
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        fig = go.Figure()

        # Add traces for different metrics
        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["duration"],
                name="Duration",
                mode="lines+markers",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["tokens"],
                name="Tokens",
                mode="lines+markers",
                yaxis="y2",
            )
        )

        # Update layout
        fig.update_layout(
            title="AI Operations Timeline",
            xaxis_title="Time",
            yaxis_title="Duration (s)",
            yaxis2=dict(title="Tokens", overlaying="y", side="right"),
            width=self.config.width,
            height=self.config.height,
            template=self.config.template,
        )

        return fig

    def plot_similarity_matrix(
        self, matrix: np.ndarray, labels: Optional[List[str]] = None
    ) -> go.Figure:
        """Plot similarity matrix heatmap"""
        fig = go.Figure(data=go.Heatmap(z=matrix, x=labels, y=labels, colorscale="Viridis"))

        fig.update_layout(
            title="Text Similarity Matrix",
            width=self.config.width,
            height=self.config.height,
            template=self.config.template,
        )

        return fig

    def plot_token_distribution(self, responses: List[Dict[str, Any]]) -> go.Figure:
        """Plot token usage distribution"""
        tokens = [r["usage"]["total_tokens"] for r in responses]

        fig = go.Figure(data=go.Histogram(x=tokens))

        fig.update_layout(
            title="Token Usage Distribution",
            xaxis_title="Tokens",
            yaxis_title="Count",
            width=self.config.width,
            height=self.config.height,
            template=self.config.template,
        )

        return fig

    def plot_performance_metrics(self, metrics: Dict[str, Any]) -> go.Figure:
        """Plot performance metrics by operation"""
        operations = metrics["operations"]

        df = pd.DataFrame(
            [
                {
                    "operation": op,
                    "success_rate": stats["success_rate"],
                    "avg_duration": stats["avg_duration"],
                    "avg_tokens": stats["avg_tokens"],
                }
                for op, stats in operations.items()
            ]
        )

        fig = go.Figure()

        # Add bars for each metric
        fig.add_trace(
            go.Bar(name="Success Rate", x=df["operation"], y=df["success_rate"], yaxis="y")
        )

        fig.add_trace(
            go.Bar(name="Avg Duration", x=df["operation"], y=df["avg_duration"], yaxis="y2")
        )

        fig.add_trace(go.Bar(name="Avg Tokens", x=df["operation"], y=df["avg_tokens"], yaxis="y3"))

        # Update layout
        fig.update_layout(
            title="Performance Metrics by Operation",
            yaxis=dict(title="Success Rate", side="left"),
            yaxis2=dict(title="Avg Duration", side="right", overlaying="y"),
            yaxis3=dict(title="Avg Tokens", side="right", overlaying="y"),
            barmode="group",
            width=self.config.width,
            height=self.config.height,
            template=self.config.template,
        )

        return fig
