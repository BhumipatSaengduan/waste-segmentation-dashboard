import numpy as np
import pytest

from app.core.preprocess import (
    hex_to_rgb,
    sanitize_filename,
    resize_image_keep_ratio,
    compute_image_hash,
    prepare_image_from_upload,
)

# pytest tests/core/test_preprocess.py -v 

class DummyUploadFile:
    """Minimal stand-in for Streamlit UploadedFile."""

    def __init__(self, name: str, data: bytes):
        self.name = name
        self._data = data

    def getvalue(self):
        return self._data

def test_hex_to_rgb_basic():
    """Hex color should be converted to an RGB tuple."""
    assert hex_to_rgb("#FF0000") == (255, 0, 0)
    assert hex_to_rgb("#00FF00") == (0, 255, 0)
    assert hex_to_rgb("#0000FF") == (0, 0, 255)

def test_sanitize_filename_removes_unsafe_chars():
    """Unsafe characters should be replaced with underscores."""
    filename = "my image@2024!.jpg"
    result = sanitize_filename(filename)

    assert result == "my_image_2024_.jpg"

def test_sanitize_filename_keeps_safe_chars():
    """Safe characters should remain unchanged."""
    filename = "image-01_test.png"
    result = sanitize_filename(filename)

    assert result == filename

def test_resize_image_keep_ratio_smaller_than_limit():
    """Image smaller than limits should not be resized."""
    img = np.zeros((100, 200, 3), dtype=np.uint8)

    resized = resize_image_keep_ratio(img, max_w=500, max_h=500)

    assert resized.shape == img.shape

def test_resize_image_keep_ratio_downscale():
    """Image larger than limits should be scaled down while keeping ratio."""
    img = np.zeros((1000, 2000, 3), dtype=np.uint8)

    resized = resize_image_keep_ratio(img, max_w=500, max_h=500)

    h, w = resized.shape[:2]

    assert w <= 500
    assert h <= 500

def test_compute_image_hash_consistency():
    """Same input bytes should always produce the same hash."""
    data = b"test image data"

    hash1 = compute_image_hash(data)
    hash2 = compute_image_hash(data)

    assert hash1 == hash2

def test_compute_image_hash_difference():
    """Different input bytes should produce different hashes."""
    hash1 = compute_image_hash(b"image one")
    hash2 = compute_image_hash(b"image two")

    assert hash1 != hash2

def test_prepare_image_from_upload_success(monkeypatch):
    """Valid uploaded image should return processed outputs."""

    dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)

    monkeypatch.setattr(
        "app.core.preprocess.cv2.imdecode",
        lambda buf, flag: dummy_image,
    )

    file = DummyUploadFile("my image!.jpg", b"fake image bytes")

    image_bgr, file_bytes, safe_name, image_hash = prepare_image_from_upload(
        file, max_width=200, max_height=200
    )

    assert image_bgr is not None
    assert file_bytes == b"fake image bytes"
    assert safe_name == "my_image_.jpg"
    assert isinstance(image_hash, str)

def test_prepare_image_from_upload_invalid_image(monkeypatch):
    """Invalid image decoding should return all None."""

    monkeypatch.setattr(
        "app.core.preprocess.cv2.imdecode",
        lambda buf, flag: None,
    )

    file = DummyUploadFile("bad.jpg", b"corrupted data")

    result = prepare_image_from_upload(file, 200, 200)

    assert result == (None, None, None, None)
