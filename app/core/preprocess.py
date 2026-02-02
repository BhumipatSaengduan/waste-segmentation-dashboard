import re
import cv2
import hashlib
import numpy as np
from .config import *

def hex_to_rgb(hex_color: str):
    """Convert hex color (#RRGGBB) to RGB tuple"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def sanitize_filename(filename):
    """Remove unsafe characters from filename"""
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", filename)

def resize_image_keep_ratio(image, max_w, max_h):
    """Resize image while keeping aspect ratio"""
    h, w = image.shape[:2]

    scale = min(max_w / w, max_h / h, 1.0)
    new_w = int(w * scale)
    new_h = int(h * scale)

    if scale < 1.0:
        image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    return image

def compute_image_hash(image_bytes):
    """Generate SHA256 hash for image content"""
    return hashlib.sha256(image_bytes).hexdigest()

def prepare_image_from_upload(uploaded_file, max_width, max_height):
    """Read and prepare image from uploaded file."""    
    file_bytes = uploaded_file.getvalue()

    image_bgr = cv2.imdecode(
        np.frombuffer(file_bytes, np.uint8),
        cv2.IMREAD_COLOR
    )

    if image_bgr is None:
        return None, None, None, None

    # Sanitize filename and compute hash
    safe_filename = sanitize_filename(uploaded_file.name)
    image_hash = compute_image_hash(file_bytes)

    # Resize keeping aspect ratio
    image_bgr = resize_image_keep_ratio(image_bgr, max_width, max_height)

    return image_bgr, file_bytes, safe_filename, image_hash
