from dataclasses import dataclass
from typing import Optional, Dict
import numpy as np

@dataclass
class BatchItemResult:
    image: str
    image_rgb: Optional[np.ndarray]
    overlay: Optional[np.ndarray]
    percentages: Optional[Dict[str, float]]
    dominant: Optional[str]
    error: Optional[str]
    saved: bool = False

@dataclass
class BatchResult:
    total_images: int
    success: int
    failed: int
    results: list[BatchItemResult]
