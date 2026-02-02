import pandas as pd
import plotly.express as px

from ..core.config import CLASS_NAMES, CLASS_COLORS

def create_composition_donut(percentages):
    """Create donut chart for waste composition"""
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
    """Create horizontal bar chart for waste proportions"""
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
