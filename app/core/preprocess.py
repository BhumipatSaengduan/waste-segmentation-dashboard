import re
import cv2
import hashlib
import numpy as np
from .config import *

def hex_to_rgb(hex_color: str):
    """
    Convert a hex color string to an RGB tuple.

    Args:
        hex_color (str): Color in hex format, e.g., "#RRGGBB".

    Returns:
        tuple: (R, G, B) values as integers 0-255.
    """
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def sanitize_filename(filename):
    """
    Replace unsafe characters in a filename with underscores.

    Args:
        filename (str): Original filename.

    Returns:
        str: Safe filename.
    """
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", filename)

def resize_image_keep_ratio(image, max_w, max_h):
    """
    Resize an image to fit within max dimensions while keeping aspect ratio.

    Args:
        image (np.ndarray): Input image array.
        max_w (int): Maximum width.
        max_h (int): Maximum height.

    Returns:
        np.ndarray: Resized image array.
    """
    h, w = image.shape[:2]

    scale = min(max_w / w, max_h / h, 1.0)
    new_w = int(w * scale)
    new_h = int(h * scale)

    if scale < 1.0:
        image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    return image

def compute_image_hash(image_bytes):
    """
    Compute a SHA256 hash of the image bytes.

    Args:
        image_bytes (bytes): Raw image bytes.

    Returns:
        str: Hexadecimal SHA256 hash.
    """
    return hashlib.sha256(image_bytes).hexdigest()

def prepare_image_from_upload(uploaded_file, max_width, max_height):
    """
    Read an uploaded file, resize, and return image and metadata.

    Args:
        uploaded_file: File-like object from upload.
        max_width (int): Maximum width for resizing.
        max_height (int): Maximum height for resizing.

    Returns:
        tuple:
            image_bgr (np.ndarray | None): Resized BGR image.
            file_bytes (bytes | None): Raw file bytes.
            safe_filename (str | None): Sanitized filename.
            image_hash (str | None): SHA256 hash of file content.
    """   
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
