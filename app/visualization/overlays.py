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
    """
    Overlay segmentation masks on an RGB image.

    Args:
        image_rgb (np.ndarray): Original image in RGB format, shape (H, W, 3).
        masks (np.ndarray): Boolean masks of detected objects, shape (N, H, W).
        classes (np.ndarray): Array of class IDs corresponding to each mask, shape (N,).
        visible_classes (list[str]): List of class names to display in the overlay.
        class_names (list[str], optional): Mapping of class IDs to display names. Defaults to CLASS_NAMES.
        class_colors (dict[str, str], optional): Hex colors for each class. Defaults to CLASS_COLORS.
        alpha (float, optional): Transparency factor for overlay (0 = invisible, 1 = fully colored). Defaults to 0.4.

    Returns:
        np.ndarray: Image with colored mask overlay, dtype=np.uint8, shape (H, W, 3).
    """
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
