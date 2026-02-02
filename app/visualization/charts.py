import pandas as pd
import plotly.express as px

from ..core.config import CLASS_NAMES, CLASS_COLORS

def create_composition_donut(percentages):
    """
    Create a donut chart showing waste composition.

    Args:
        percentages (dict): Dictionary mapping each waste class to its percentage.

    Returns:
        plotly.graph_objects.Figure: Donut chart figure.
    """
    df_vis = pd.DataFrame({
        "Class": CLASS_NAMES,
        "Percentage (%)": [percentages[c] for c in CLASS_NAMES]
    })

    fig = px.pie(
        df_vis,
        names="Class",
        values="Percentage (%)",
        hole=0.5,
        color="Class",
        color_discrete_map=CLASS_COLORS,
        title="Waste Composition",
    )
    return fig

def create_proportion_bar(percentages):
    """
    Create a horizontal bar chart for waste class proportions.

    Args:
        percentages (dict): Dictionary mapping each waste class to its percentage.

    Returns:
        plotly.graph_objects.Figure: Horizontal bar chart figure.
    """
    df_vis = pd.DataFrame({
        "Class": CLASS_NAMES,
        "Percentage (%)": [percentages[c] for c in CLASS_NAMES]
    })

    fig = px.bar(
        df_vis.sort_values("Percentage (%)"),
        x="Percentage (%)",
        y="Class",
        orientation="h",
        color="Class",
        color_discrete_map=CLASS_COLORS,
        title="Waste Proportion by Class"
    )
    return fig
