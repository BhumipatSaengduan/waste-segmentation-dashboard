import numpy as np
import pytest

from app.batch.processor import run_batch

# pytest tests/batch/test_processor.py -v     

class DummyMasks:
    def __init__(self):
        self.data = self

    def __len__(self):
        """Simulate non-empty mask tensor."""
        return 1

    def cpu(self):
        return self

    def numpy(self):
        return np.ones((1, 2, 2))

class DummyBoxes:
    def __init__(self):
        self.cls = self

    def cpu(self):
        return self

    def numpy(self):
        return np.array([0])

class DummyInference:
    def __init__(self):
        self.masks = DummyMasks()
        self.boxes = DummyBoxes()

def test_run_batch_empty_files():
    """Running batch with no files should return empty result."""
    result = run_batch(
        files=[],
        model=None,
        conf_thres=0.5,
        visible_classes=[],
        max_width=640,
        max_height=480,
    )

    assert result.total_images == 0
    assert result.success == 0
    assert result.failed == 0
    assert result.results == []

def test_run_batch_single_success(monkeypatch):
    """A single valid image should produce one successful result."""

    # --- mocks ---
    monkeypatch.setattr(
        "app.batch.processor.prepare_image_from_upload",
        lambda file, w, h: (np.zeros((2, 2, 3)), None, "image.jpg", None),
    )

    monkeypatch.setattr(
        "app.batch.processor.run_inference",
        lambda model, img, conf: DummyInference(),
    )

    monkeypatch.setattr(
        "app.batch.processor.calculate_pixel_area",
        lambda masks, classes: {"Plastic": 4},
    )

    monkeypatch.setattr(
        "app.batch.processor.calculate_percentage",
        lambda area: {"Plastic": 100.0},
    )

    monkeypatch.setattr(
        "app.batch.processor.create_mask_overlay",
        lambda img, masks, classes, visible: img,
    )

    monkeypatch.setattr(
        "app.batch.processor.cv2.cvtColor",
        lambda img, code: img,
    )

    # --- run ---
    dummy_file = type("File", (), {"name": "test.jpg"})()

    result = run_batch(
        files=[dummy_file],
        model=None,
        conf_thres=0.5,
        visible_classes=[],
        max_width=640,
        max_height=480,
    )

    assert result.total_images == 1
    assert result.success == 1
    assert result.failed == 0

    item = result.results[0]
    assert item.error is None
    assert item.dominant == "Plastic"
