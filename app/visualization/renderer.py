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
    Overlay segmentation masks on an RGB image.

    Args:
        image_rgb (np.ndarray): Original image in RGB format, shape (H, W, 3).
        masks (np.ndarray): Boolean masks of detected objects, shape (N, H, W).
        classes (np.ndarray): Array of class IDs corresponding to each mask, shape (N,).
        visible_classes (list[str]): List of class names to display in the overlay.
        class_names (list[str], optional): Mapping of class IDs to display names. Defaults to CLASS_NAMES.
        class_colors (dict[str, str], optional): Hex colors for each class. Defaults to CLASS_COLORS.
        alpha (float, optional): Transparency factor for overlay (0 = invisible, 1 = fully colored). Defaults to 0.4.

    Returns:
        np.ndarray: Image with colored mask overlay, dtype=np.uint8, shape (H, W, 3).
    """
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
