import streamlit as st
import cv2
import json
import zipfile
from io import BytesIO
from datetime import datetime

from ..batch.processor import run_batch
from ..core.config import MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT, MODEL_VERSION
from ..visualization.renderer import render_analysis_result
from ..db.database import save_to_db

def run_batch_analysis(uploaded_files, model, conf_thres, visible_classes):
    """Run batch analysis workflow."""
    st.subheader("📦 Batch Processing")
    st.info("📦 Processing batch images...")

    batch_result = run_batch(
        files=uploaded_files,
        model=model,
        conf_thres=conf_thres,
        visible_classes=visible_classes,
        max_width=MAX_IMAGE_WIDTH,
        max_height=MAX_IMAGE_HEIGHT
    )

    st.success("✅ Batch processing completed")

    st.subheader("📊 Batch Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Images", batch_result.total_images)
    col2.metric("Success", batch_result.success)
    col3.metric("Failed", batch_result.failed)

    st.caption("Batch inference completed. Results shown below.")

    st.divider()
    st.subheader("🖼️ Batch Results")

    for idx, item in enumerate(batch_result.results, start=1):
        with st.expander(f"📷 [{idx}] {item.image}"):
            if item.error is not None:
                st.error(f"❌ {item.error}")
                continue

            render_analysis_result(
                image_rgb=item.image_rgb,
                overlay=item.overlay,
                percentages=item.percentages,
                dominant=item.dominant,
                conf_thres=conf_thres,
                visible_classes=visible_classes,
                idx=idx
            )

            st.divider()

    st.subheader("📤 Batch Export")

    # ===== Create ZIP for overlay images =====
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for item in batch_result.results:
            if item.error is None:
                overlay_bgr = cv2.cvtColor(item.overlay, cv2.COLOR_RGB2BGR)
                success, buffer = cv2.imencode(".png", overlay_bgr)

                if success:
                    zip_file.writestr(
                        f"{item.image}_overlay.png",
                        buffer.tobytes()
                    )

    zip_buffer.seek(0)

    has_overlays = batch_result.success > 0

    st.download_button(
        label="🗂️ Download ALL Overlay Images (ZIP)",
        data=zip_buffer,
        file_name=f"batch_overlays_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
        mime="application/zip",
        use_container_width=True,
        disabled=not has_overlays
    )

    batch_summary = {
        "batch_datetime": datetime.now().isoformat(),
        "total_images": batch_result.total_images,
        "success": batch_result.success,
        "failed": batch_result.failed,
        "confidence_threshold": conf_thres,
        "model_version": MODEL_VERSION,
        "results": []
    }

    for item in batch_result.results:
        if item.error is None:
            batch_summary["results"].append({
                "image": item.image,
                "dominant_class": item.dominant,
                "percentages": item.percentages
            })
        else:
            batch_summary["results"].append({
                "image": item.image,
                "error": item.error
            })

    json_bytes = json.dumps(batch_summary, indent=2).encode("utf-8")

    st.download_button(
        label="📄 Download Batch JSON Summary",
        data=json_bytes,
        file_name=f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        use_container_width=True
    )

    st.divider()
    st.subheader("💾 Batch Save")

    can_save = batch_result.success > 0

    if st.button(
        "💾 Save ALL Successful Results to History",
        use_container_width=True,
        disabled=not can_save
    ):
        with st.spinner("Saving batch results to database..."):
            saved_count = 0

            for item in batch_result.results:
                if item.error is None and not item.saved:
                    save_to_db(
                        item.image,
                        None,
                        conf_thres,
                        item.percentages
                    )
                    item.saved = True
                    saved_count += 1

        st.success(f"✅ Saved {saved_count} records to history")
