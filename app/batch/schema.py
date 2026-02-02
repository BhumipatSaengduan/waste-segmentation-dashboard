from dataclasses import dataclass
from typing import Optional, Dict
import numpy as np

@dataclass
class BatchItemResult:
    """
    Stores results for a single processed image.

    Attributes:
        image (str): Original or saved image filename.
        image_rgb (Optional[np.ndarray]): RGB image array.
        overlay (Optional[np.ndarray]): Image overlay with detected masks.
        percentages (Optional[Dict[str, float]]): Class-wise pixel percentage.
        dominant (Optional[str]): Dominant class in the image.
        error (Optional[str]): Error message if processing failed.
        saved (bool): Whether the result image was saved. Default is False.
    """
    image: str
    image_rgb: Optional[np.ndarray]
    overlay: Optional[np.ndarray]
    percentages: Optional[Dict[str, float]]
    dominant: Optional[str]
    error: Optional[str]
    saved: bool = False

@dataclass
class BatchResult:
    """
    Stores results for a single processed image.

    Attributes:
        image (str): Original or saved image filename.
        image_rgb (Optional[np.ndarray]): RGB image array.
        overlay (Optional[np.ndarray]): Image overlay with detected masks.
        percentages (Optional[Dict[str, float]]): Class-wise pixel percentage.
        dominant (Optional[str]): Dominant class in the image.
        error (Optional[str]): Error message if processing failed.
        saved (bool): Whether the result image was saved. Default is False.
    """
    total_images: int
    success: int
    failed: int
    results: list[BatchItemResult]
