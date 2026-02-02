import streamlit as st

# RUN APP: streamlit run main.py

# =========================
# LOGGER
# =========================
from app.core.logger import get_logger
logger = get_logger("main")

# =========================
# CORE
# =========================
from app.core.config import *
from app.core.model import load_model_safe
from app.core.validation import validate_uploaded_files

# =========================
# DB
# =========================
from app.db.schema import (
    create_tables,
    migrate_db,
    backfill_metadata
)

# =========================
# UI
# =========================
from app.ui import (
    render_sidebar,
    run_single_image_analysis,
    run_batch_analysis,
    render_data_summary,
    render_history_section,
    render_time_series_section,
    render_danger_zone
)

# =========================
# STREAMLIT SETUP
# =========================
st.set_page_config(
    page_title="Waste Segmentation Dashboard",
    layout="wide",
    page_icon="♻️",
    initial_sidebar_state="expanded"
)

logger.info("========== Application Started ==========")


# =========================
# DATABASE INITIALIZATION
# =========================
create_tables()
migrate_db()
backfill_metadata()

logger.info("Database initialized")

# =========================
# SESSION STATE
# =========================
if "confirm_action" not in st.session_state:
    st.session_state.confirm_action = None

# =========================
# SIDEBAR & FILE UPLOAD
# =========================
mode, visible_classes, conf_thres, uploaded = render_sidebar()

# =========================
# FILE COUNT (SAFE)
# =========================
if uploaded is None:
    file_count = 0
elif isinstance(uploaded, list):
    file_count = len(uploaded)
else:
    file_count = 1

logger.info(
    f"Sidebar input | mode={mode}, "
    f"files_uploaded={file_count}, "
    f"conf_thres={conf_thres}"
)

# =========================
# FILE SIZE VALIDATION
# =========================
validate_uploaded_files(uploaded, MAX_FILE_SIZE_MB)

# =========================
# LOAD MODEL
# =========================
model = load_model_safe(MODEL_PATH)

if model is None:
    logger.error("Model loading failed")
    st.stop()

logger.info("Model loaded successfully")

# =========================
# MAIN ANALYSIS WORKFLOW
# =========================
if mode == "Single Image" and uploaded:
    logger.info("Running single image analysis")
    run_single_image_analysis(uploaded, model, conf_thres, visible_classes)

elif mode == "Batch" and uploaded:
    logger.info("Running batch image analysis")
    run_batch_analysis(uploaded, model, conf_thres, visible_classes)

else:
    logger.info("No analysis executed")

# =========================
# DATA SUMMARY & HISTORY
# =========================
render_data_summary()
render_history_section()
render_time_series_section()

logger.info("Rendered summary, history, and time series")

# =========================
# DANGER ZONE
# =========================
render_danger_zone()

logger.info("UI fully rendered")
