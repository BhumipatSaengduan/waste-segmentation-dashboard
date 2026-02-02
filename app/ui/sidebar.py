import streamlit as st
from ..core.config import CLASS_NAMES

def render_sidebar(mode_options=["Single Image", "Batch"]):
    """
    Render the Streamlit sidebar with analysis controls.

    Features:
        - Select analysis mode (Single Image or Batch).
        - Choose which mask classes to display.
        - Set confidence threshold for detections.
        - Upload image(s) depending on selected mode.

    Args:
        mode_options (list, optional): List of analysis mode options. Defaults to ["Single Image", "Batch"].

    Returns:
        tuple: (mode, visible_classes, conf_thres, uploaded_files)
    """
    st.sidebar.header("Controls")

    # === MODE TOGGLE ===
    mode = st.sidebar.radio(
        "Analysis Mode",
        options=mode_options,
        index=0
    )

    st.sidebar.divider()
    st.sidebar.subheader("Mask Visualization")

    visible_classes = st.sidebar.multiselect(
        "Show Mask Classes",
        CLASS_NAMES,
        default=CLASS_NAMES,
        key="visible_mask_classes"
    )

    conf_thres = st.sidebar.slider(
        "Confidence Threshold",
        min_value=0.05,
        max_value=1.0,
        value=0.25,
        step=0.05
    )

    if mode == "Single Image":
        uploaded = st.file_uploader(
            "Upload an image",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=False
        )
    else:
        uploaded = st.file_uploader(
            "Upload images (Batch)",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True
        )
        st.info(
            "📦 Batch mode processes multiple images sequentially. "
            "Results will be summarized after completion."
        )

    return mode, visible_classes, conf_thres, uploaded
