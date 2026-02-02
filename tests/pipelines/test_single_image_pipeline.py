import numpy as np
import pytest

from app.pipelines.single_image import run_single_image_pipeline

# pytest tests/db/test_database_contract.py -v

class DummyFile:
    def __init__(self, name="test.jpg"):
        self.name = name

    def getvalue(self):
        return b"fake-bytes"

class FakeTensor:
    """Minimal torch-like tensor mock."""

    def __init__(self, array):
        self._array = array

    def cpu(self):
        return self

    def numpy(self):
        return self._array

    def __len__(self):
        return len(self._array)

class DummyInference:
    def __init__(self):
        self.masks = type(
            "Masks",
            (),
            {"data": FakeTensor(np.ones((1, 2, 2)))},
        )()
        self.boxes = type(
            "Boxes",
            (),
            {"cls": FakeTensor(np.array([0]))},
        )()

def test_single_image_pipeline_success(monkeypatch):
    """Pipeline should return correct SingleImageResult."""

    monkeypatch.setattr(
        "app.pipelines.single_image.prepare_image_from_upload",
        lambda f, w, h: (np.zeros((2, 2, 3), dtype=np.uint8), b"x", "image.jpg", "hash123"),
    )

    monkeypatch.setattr(
        "app.pipelines.single_image.run_inference",
        lambda m, img, c: DummyInference(),
    )

    monkeypatch.setattr(
        "app.pipelines.single_image.calculate_pixel_area",
        lambda m, c: {"Plastic": 4},
    )

    monkeypatch.setattr(
        "app.pipelines.single_image.calculate_percentage",
        lambda a: {"Plastic": 100.0},
    )

    monkeypatch.setattr(
        "app.pipelines.single_image.create_mask_overlay",
        lambda img, m, c, v, **kwargs: img
    )

    monkeypatch.setattr(
        "app.pipelines.single_image.cv2.cvtColor",
        lambda img, code: img,
    )

    result = run_single_image_pipeline(
        DummyFile(),
        model=None,
        conf_thres=0.5,
        visible_classes=[],
        max_width=640,
        max_height=480,
    )

    assert result.image_name == "image.jpg"
    assert result.image_hash == "hash123"
    assert result.dominant == "Plastic"
    assert result.percentages == {"Plastic": 100.0}
    assert result.overlay is not None
