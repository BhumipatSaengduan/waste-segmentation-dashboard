from dataclasses import dataclass
import numpy as np
from typing import Dict, Optional

@dataclass
class SingleImageResult:
    """
    Stores the result of a single image analysis pipeline.

    Attributes:
        image_name (str): Filename of the analyzed image.
        image_hash (str): SHA256 hash of the image content.
        image_rgb (np.ndarray): Original image in RGB format.
        overlay (np.ndarray): Image overlay with detected masks.
        percentages (Dict[str, float]): Class-wise pixel percentages.
        dominant (str): Dominant class in the image.
        overlay_bytes (Optional[bytes]): Optional overlay image in bytes.
        datetime (Optional[str]): Optional timestamp of analysis.
    """
    image_name: str
    image_hash: str
    image_rgb: np.ndarray
    overlay: np.ndarray
    percentages: Dict[str, float]
    dominant: str
    overlay_bytes: Optional[bytes] = None  
    datetime: Optional[str] = None         
