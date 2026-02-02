import numpy as np
import pytest

from app.core.postprocess import (
    calculate_pixel_area,
    calculate_percentage
)

# pytest tests/core/test_postprocess.py -v 

def test_calculate_pixel_area_single_class():
    """Test pixel area calculation for a single mask belong to one class."""
    masks = np.array([
        [[1, 1],
         [1, 1]]
    ])

    classes = np.array([0])

    result = calculate_pixel_area(masks, classes)

    assert result["Metal"] == 4
    assert sum(result.values()) == 4

def test_calculate_pixel_area_multiple_classes():
    """Test pixel area calculation when multiple masks belong to different classes."""
    masks = np.array([
        [[0.9, 0.0],
         [0.8, 0.0]],   # 2 active pixels → class 0

        [[0.0, 0.7],
         [0.0, 0.6]]    # 2 active pixels → class 1
    ])

    classes = np.array([0, 1])

    result = calculate_pixel_area(masks, classes)

    # Class index 0 → "Metal"
    assert result["Metal"] == 2

    # Class index 1 → "Plastic"
    assert result["Mixed waste"] == 2

def test_calculate_percentage_normal_case():
    """Test percentage calculation from pixel areas."""
    pixel_area = {
        0: 25,
        1: 75
    }

    result = calculate_percentage(pixel_area)

    assert result[0] == 25.0
    assert result[1] == 75.0

def test_calculate_percentage_zero_total():
    """Test percentage calculation when no pixel data is provided."""
    pixel_area = {}

    result = calculate_percentage(pixel_area)

    assert result == {}

def test_calculate_percentage_sum_close_to_100():
    """Ensure that calculated percentages always sum up to 100%."""
    pixel_area = {
        0: 1,
        1: 1,
        2: 2
    }

    result = calculate_percentage(pixel_area)

    total_percentage = sum(result.values())

    assert abs(total_percentage - 100.0) < 1e-6
