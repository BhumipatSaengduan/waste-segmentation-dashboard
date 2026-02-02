import cv2
from typing import List

from ..core.logger import get_logger
from ..core.preprocess import prepare_image_from_upload
from ..core.inference import run_inference
from ..core.postprocess import calculate_pixel_area, calculate_percentage
from ..visualization.overlays import create_mask_overlay
from .schema import BatchResult, BatchItemResult

# =========================
# LOGGER
# =========================
logger = get_logger("batch.processor")

def run_batch(
    files: List,
    model,
    conf_thres: float,
    visible_classes: list,
    max_width: int,
    max_height: int,
):
    """
    Process a batch of images: prepare, run inference, post-process, and create overlays.

    Args:
        files (List): List of image files to process.
        model: Trained model for inference.
        conf_thres (float): Confidence threshold for detection.
        visible_classes (list): Classes to include in overlay visualization.
        max_width (int): Maximum image width for resizing.
        max_height (int): Maximum image height for resizing.

    Returns:
        BatchResult: Summary of batch processing with per-image results.
    """
    total_files = len(files)
    logger.info(f"Start batch processing | total_files={total_files} | conf={conf_thres}")

    results = []

    for idx, file in enumerate(files, start=1):
        filename = getattr(file, "name", "unknown")
        logger.info(f"[{idx}/{total_files}] Processing image | name={filename}")

        try:
            # -------------------------
            # Prepare image
            # -------------------------
            image_bgr, _, safe_filename, _ = prepare_image_from_upload(
                file, max_width, max_height
            )

            if image_bgr is None:
                logger.warning(f"[{idx}] Invalid image")
                raise ValueError("Invalid image")

            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

            # -------------------------
            # Run inference
            # -------------------------
            inference = run_inference(model, image_rgb, conf_thres)

            if (
                inference is None
                or inference.masks is None
                or len(inference.masks.data) == 0
            ):
                logger.warning(f"[{idx}] No detection")
                raise ValueError("No detection")

            masks = inference.masks.data.cpu().numpy()
            classes = inference.boxes.cls.cpu().numpy()

            # -------------------------
            # Post-process
            # -------------------------
            percentages = calculate_percentage(
                calculate_pixel_area(masks, classes)
            )
            dominant = max(percentages, key=percentages.get)

            logger.info(
                f"[{idx}] Detection success | dominant={dominant} | percentages={percentages}"
            )

            # -------------------------
            # Create overlay
            # -------------------------
            overlay = create_mask_overlay(
                image_rgb, masks, classes, visible_classes
            )

            results.append(
                BatchItemResult(
                    image=safe_filename,
                    image_rgb=image_rgb,
                    overlay=overlay,
                    percentages=percentages,
                    dominant=dominant,
                    error=None
                )
            )

        except Exception as e:
            logger.exception(
                f"[{idx}] Processing failed | image={filename} | error={str(e)}"
            )

            results.append(
                BatchItemResult(
                    image=filename,
                    image_rgb=None,
                    overlay=None,
                    percentages=None,
                    dominant=None,
                    error=str(e)
                )
            )

    success = sum(1 for r in results if r.error is None)
    failed = total_files - success

    logger.info(
        f"Batch finished | total={total_files} | success={success} | failed={failed}"
    )

    return BatchResult(
        total_images=total_files,
        success=success,
        failed=failed,
        results=results
    )
