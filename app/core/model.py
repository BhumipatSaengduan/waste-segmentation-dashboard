import streamlit as st
from ultralytics import YOLO

@st.cache_resource
def load_model_safe(model_path):
    """
    Load a YOLO model safely with Streamlit spinner and error handling.

    Args:
        model_path (str): Path to the YOLO model file.

    Returns:
        YOLO: Loaded YOLO model instance, or None if loading fails.
    """
    try:
        with st.spinner("Loading model..."):
            model = YOLO(model_path)
        return model
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return None
    