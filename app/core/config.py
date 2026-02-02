from pathlib import Path
from datetime import date, timedelta

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "v8n_finetuned" / "best.pt" # v11s_finetuned
RESULT_DIR = BASE_DIR / "results"
RESULT_DIR.mkdir(exist_ok=True)

# Storage
CSV_PATH = RESULT_DIR / "analysis_history.csv"
DB_PATH = RESULT_DIR / "analysis_history.db"

# File upload limits
MAX_FILE_SIZE_MB = 20
MAX_IMAGE_WIDTH = 1280
MAX_IMAGE_HEIGHT = 1280

# Model settings
IMG_SIZE = 640
MODEL_VERSION = "yolov8-finetuned-v1"
IMAGE_SOURCE = "upload"

# Waste classes
CLASS_NAMES = ['Metal', 'Mixed waste', 'Plastic', 'Paper&Cardboard',  'Wood']

CLASS_COLORS = {
    'Metal': '#B0B0B0',
    'Mixed waste': "#E95500",
    'Plastic': '#3498DB',
    'Paper&Cardboard': '#F7DC6F',
    'Wood': '#8E5A2B'
}

# Database column mapping
DB_CLASS_MAP = {
    "metal": "Metal",
    "mixed_waste": "Mixed waste",
    "plastic": "Plastic",
    "paper_cardboard": "Paper&Cardboard",
    "wood": "Wood"
}

# Date Defaults
TODAY = date.today()
DEFAULT_START_DATE = TODAY - timedelta(days=30)
DEFAULT_END_DATE = TODAY
