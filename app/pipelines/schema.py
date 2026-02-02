from dataclasses import dataclass
import numpy as np
from typing import Dict, Optional

@dataclass
class SingleImageResult:
    """Pure result of single image analysis pipeline."""

    image_name: str
    image_hash: str
    image_rgb: np.ndarray
    overlay: np.ndarray
    percentages: Dict[str, float]
    dominant: str
    overlay_bytes: Optional[bytes] = None  # Overlay
    datetime: Optional[str] = None         # Timestamp 
