import cv2
import io
from PIL import Image
from datetime import datetime

from ..core.logger import get_logger
from ..core.preprocess import prepare_image_from_upload
from ..core.inference import run_inference
from ..core.postprocess import calculate_pixel_area, calculate_percentage
from ..visualization.overlays import create_mask_overlay
from .schema import SingleImageResult

from ..core.config import CLASS_NAMES ,CLASS_COLORS, MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT  

# =========================
# LOGGER
# =========================
logger = get_logger("pipeline.single_image")

def run_single_image_pipeline(
    uploaded_file,
    model,
    conf_thres,
    visible_classes,
    max_width=MAX_IMAGE_WIDTH,
    max_height=MAX_IMAGE_HEIGHT,
):
    """
    Complete single-image analysis pipeline: prepare image, run inference,
    post-process results, and create overlay.

    Args:
        uploaded_file: Uploaded file object from Streamlit.
        model: Trained YOLO model.
        conf_thres (float): Confidence threshold for detections.
        visible_classes (list): Classes to include in overlay visualization.
        max_width (int, optional): Maximum image width. Defaults to MAX_IMAGE_WIDTH.
        max_height (int, optional): Maximum image height. Defaults to MAX_IMAGE_HEIGHT.

    Returns:
        SingleImageResult: Object containing processed image, overlay, 
                           class percentages, dominant class, and timestamp.

    Raises:
        ValueError: If the image is invalid or no detection is found.
    """
    try:
        # =========================
        # START PIPELINE
        # =========================
        logger.info(
            f"Start processing | file={getattr(uploaded_file, 'name', 'unknown')} | conf={conf_thres}"
        )

        # -------------------------
        # Prepare image
        # -------------------------
        image_bgr, _, safe_filename, image_hash = prepare_image_from_upload(
            uploaded_file, max_width, max_height
        )

        if image_bgr is None:
            logger.error("Invalid image upload")
            raise ValueError("Invalid image")

        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        logger.info(f"Image prepared | name={safe_filename} | hash={image_hash}")

        # -------------------------
        # Run inference
        # -------------------------
        logger.info("Running inference")
        results = run_inference(model, image_rgb, conf_thres)

        if results is None or results.masks is None or len(results.masks.data) == 0:
            logger.warning("No detection found")
            raise ValueError("No detection")

        masks = results.masks.data.cpu().numpy()
        classes = results.boxes.cls.cpu().numpy()

        # Check mask ↔ class
        if model is not None and hasattr(model, "names"):
            logger.warning(f"MODEL NAMES: {model.names}")
            logger.warning("=== MASK CLS CHECK ===")
            for i in range(min(5, len(classes))):
                cls_id = int(classes[i])
                logger.warning(
            f"mask[{i}] -> cls={cls_id}, name={model.names.get(cls_id)}"
            )


        logger.info(
            f"Inference success | masks={len(masks)} | classes={set(classes.tolist())}"
        )

        # -------------------------
        # Post-process
        # -------------------------
        percentages = calculate_percentage(
            calculate_pixel_area(masks, classes)
        )
        dominant = max(percentages, key=percentages.get)

        logger.info(
            f"Postprocess done | dominant={dominant} | percentages={percentages}"
        )

        # -------------------------
        # Create overlay
        # -------------------------
        overlay = create_mask_overlay(
            image_rgb,
            masks,
            classes,
            visible_classes,
            class_names=CLASS_NAMES,
            class_colors=CLASS_COLORS
        )

        logger.info("Overlay created")
        
        # -------------------------
        # Convert overlay to bytes
        # -------------------------
        overlay_pil = Image.fromarray(overlay)
        buf = io.BytesIO()
        overlay_pil.save(buf, format="PNG")
        overlay_bytes = buf.getvalue()

        result_datetime = datetime.now().isoformat()

        logger.info(f"Finished processing | image={safe_filename}")

        return SingleImageResult(
            image_name=safe_filename,
            image_hash=image_hash,
            image_rgb=image_rgb,
            overlay=overlay,
            overlay_bytes=overlay_bytes,
            percentages=percentages,
            dominant=dominant,
            datetime=result_datetime,
        )

    except Exception as e:
        logger.exception(
            f"Pipeline failed | file={getattr(uploaded_file, 'name', 'unknown')} | error={str(e)}"
        )
        raise
