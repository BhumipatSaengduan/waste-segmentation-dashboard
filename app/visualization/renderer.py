import streamlit as st

from .charts import (
    create_composition_donut,
    create_proportion_bar
)

def render_analysis_result(
    *,
    image_rgb,
    overlay,
    percentages,
    dominant,
    conf_thres,
    visible_classes,
    idx
):
    """
    Shared renderer for Single & Batch results
    idx: unique identifier for Streamlit keys
    """

    # === IMAGES ===
    c = st.columns([1, 2, 2, 1])
    c[1].image(
        image_rgb,
        caption="Original Image",
        use_container_width=True
    )
    c[2].image(
        overlay,
        caption="Segmentation Result",
        use_container_width=True
    )

    if len(visible_classes) == 0:
        st.warning("All mask classes are hidden. No overlay is displayed.")

    # === METRICS ===
    k1, k2, k3 = st.columns(3)
    k1.metric("Dominant Waste Type", dominant)
    k2.metric(
        "Max Proportion",
        f"{percentages[dominant]:.1f}%"
    )
    k3.metric("Confidence", f"{conf_thres:.2f}")

    # === CHARTS ===
    donut = create_composition_donut(percentages)
    bar = create_proportion_bar(percentages)

    c1, c2 = st.columns(2)
    c1.plotly_chart(
        donut,
        use_container_width=True,
        key=f"donut_{idx}"
    )
    c2.plotly_chart(
        bar,
        use_container_width=True,
        key=f"bar_{idx}"
    )
