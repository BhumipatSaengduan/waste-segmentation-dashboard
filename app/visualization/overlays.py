import numpy as np
from ..core.preprocess import hex_to_rgb
from ..core.config import CLASS_NAMES, CLASS_COLORS, DB_CLASS_MAP

def create_mask_overlay(
    image_rgb,
    masks,
    classes,
    visible_classes,
    class_names=CLASS_NAMES,
    class_colors=CLASS_COLORS,
    alpha=0.4
):
    """Create mask overlay visualization on original image"""

    overlay = image_rgb.astype(np.float32).copy()

    for mask, cls_id in zip(masks, classes):
        display_name = class_names[int(cls_id)]

        # Skip hidden classes
        if display_name not in visible_classes:
            continue

        color_rgb = np.array(
            hex_to_rgb(class_colors[display_name]),
            dtype=np.float32
        )

        m = mask.astype(bool)
        overlay[m] = (1 - alpha) * overlay[m] + alpha * color_rgb

    overlay = np.clip(overlay, 0, 255).astype(np.uint8)
    return overlay
