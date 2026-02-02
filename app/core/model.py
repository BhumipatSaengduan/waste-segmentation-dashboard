import streamlit as st
from ultralytics import YOLO

@st.cache_resource
def load_model_safe(model_path):
    """Load YOLO model with spinner and error handling"""
    try:
        with st.spinner("Loading model..."):
            model = YOLO(model_path)
        return model
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return None
    