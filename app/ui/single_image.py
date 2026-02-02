import streamlit as st
import json

from ..core.logger import get_logger
from ..pipelines.single_image import run_single_image_pipeline
from ..core.config import (
    MAX_IMAGE_WIDTH,
    MAX_IMAGE_HEIGHT,
)
from ..visualization.renderer import render_analysis_result
from ..db.database import save_to_db

# =========================
# LOGGER
# =========================
logger = get_logger("ui.log")

def run_single_image_analysis(uploaded_files, model, conf_thres, visible_classes):
    """
    Streamlit UI wrapper for single image analysis workflow.

    Steps:
        1. Run the single-image pipeline (preprocess, inference, postprocess, overlay).
        2. Display image preview.
        3. Render analysis results with overlays and class percentages.
        4. Provide options to save results to database.
        5. Provide options to export overlay image and JSON summary.

    Args:
        uploaded_files: Single or list of uploaded image files.
        model: Trained YOLO model.
        conf_thres (float): Confidence threshold for detections.
        visible_classes (list): Classes to display in overlay visualization.
    """
    files = uploaded_files if isinstance(uploaded_files, list) else [uploaded_files]

    for uploaded_file in files:
        logger.info(
            f"Single image analysis started | "
            f"file={getattr(uploaded_file, 'name', 'unknown')}"
        )

        try:
            result = run_single_image_pipeline(
                uploaded_file=uploaded_file,
                model=model,
                conf_thres=conf_thres,
                visible_classes=visible_classes,
                max_width=MAX_IMAGE_WIDTH,
                max_height=MAX_IMAGE_HEIGHT,
            )

            logger.info(
                f"Analysis success | image={result.image_name} | dominant={result.dominant}"
            )

        except ValueError as e:
            logger.warning(
                f"Analysis failed | reason={str(e)}"
            )
            st.error(str(e))
            st.stop()

        # =========================
        # PREVIEW
        # =========================
        st.image(
            result.image_rgb,
            caption=f"Preview: {result.image_name}",
            use_container_width=True,
        )

        # =========================
        # RENDER ANALYSIS
        render_analysis_result(
            image_rgb=result.image_rgb,
            overlay=result.overlay,
            percentages=result.percentages,
            dominant=result.dominant,
            conf_thres=conf_thres,
            visible_classes=visible_classes,
            idx="single",
        )

        # =========================
        # SAVE RESULT
        if st.button("💾 Save Result to History", use_container_width=True):
            logger.info(f"User clicked save | image={result.image_name}")

            with st.spinner("Saving result..."):
                try:
                    save_to_db(
                        result.image_name,
                        result.image_hash,
                        conf_thres,
                        result.percentages,
                    )
                    logger.info(
                        f"Save success | image={result.image_name}"
                    )
                    st.success("Saved successfully.")

                except Exception as e:
                    logger.error(
                        f"Save failed | image={result.image_name} | error={str(e)}",
                        exc_info=True
                    )
                    st.error("Failed to save result.")

        # =========================
        # EXPORT
        _render_export(result, conf_thres)

def _render_export(result, conf_thres):
    st.divider()
    st.subheader("📤 Export Results")

    logger.info(f"Export section rendered | image={result.image_name}")

    col_img, col_json = st.columns(2)

    # Overlay image download
    with col_img:
        st.download_button(
            label="🖼️ Overlay Image",
            data=result.overlay_bytes,
            file_name=f"{result.image_name}_overlay.png",
            mime="image/png",
            use_container_width=True
        )

    # JSON summary download
    summary = {
        "image": result.image_name,
        "image_hash": result.image_hash,
        "datetime": result.datetime,
        "confidence_threshold": conf_thres,
        "dominant_class": result.dominant,
        "percentages": result.percentages
    }

    json_bytes = json.dumps(summary, indent=2).encode("utf-8")

    with col_json:
        st.download_button(
            label="📄 JSON Summary",
            data=json_bytes,
            file_name=f"{result.image_name}_summary.json",
            mime="application/json",
            use_container_width=True
        )
