import plotly.graph_objects as go
import numpy as np
from typing import List, Dict


def create_coverage_heatmap(
    aspects: List[Dict],
    retrieved_chunks: List[Dict],
    similarity_matrix: np.ndarray
):
    """
    Create an Aspect × Chunk heatmap using similarity scores.
    """

    aspect_labels = [a["aspect_text"] for a in aspects]
    chunk_labels = [c["chunk_id"] for c in retrieved_chunks]

    fig = go.Figure(
        data=go.Heatmap(
            z=similarity_matrix,
            x=chunk_labels,
            y=aspect_labels,
            colorscale="RdYlGn",
            zmin=0,
            zmax=1,
            colorbar=dict(title="Similarity")
        )
    )

    fig.update_layout(
        title="Aspect × Retrieved Chunk Coverage Heatmap",
        xaxis_title="Retrieved Chunks",
        yaxis_title="Query Aspects"
    )

    return fig
