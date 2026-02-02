import streamlit as st
from .config import *
from ..core.logger import get_logger

logger = get_logger("core.inference")

def run_inference(model, image_rgb, conf_thres):
    """
    Run YOLO segmentation inference on a single image.

    Args:
        model: Trained YOLO model.
        image_rgb: RGB image as a NumPy array.
        conf_thres: Confidence threshold for detections.

    Returns:
        Inference result object with masks, boxes, and class predictions,
        or None if an error occurs.
    """
    model.model.eval()
    
    try:
        if not hasattr(run_inference, "_printed"):
            logger.warning("=== MODEL CLASS NAMES ===")
            for k, v in model.names.items():
                logger.warning(f"class_id={k} -> {v}")
            run_inference._printed = True

        results = model.predict(
            image_rgb,
            conf=conf_thres,
            imgsz=IMG_SIZE,
            save=False
        )[0]
        return results

    except Exception as e:
        st.error(f"Inference error: {e}")
        return None
