from .config import CLASS_NAMES

def threshold_label(conf):
    """
    Determine label based on confidence value.

    Args:
        conf (float): Confidence score (0.0-1.0).

    Returns:
        str: "Strict", "Balanced", or "Loose" depending on threshold.
    """
    if conf >= 0.5:
        return "Strict"
    elif conf >= 0.25:
        return "Balanced"
    return "Loose"

def calculate_pixel_area(masks, classes):
    """
    Calculate pixel area per class from segmentation masks.

    Args:
        masks (np.ndarray): Segmentation masks of shape (N, H, W).
        classes (np.ndarray): Class indices for each mask.

    Returns:
        dict: Mapping from class name to total pixel count.
    """
    # Initialize result dict (display names)
    area_by_class = {c: 0 for c in CLASS_NAMES}

    # Basic shape validation
    if masks.ndim != 3:
        raise ValueError("Masks must have shape (N, H, W)")

    if len(masks) != len(classes):
        raise ValueError("Masks and classes length mismatch")

    # Convert masks to boolean if needed
    masks_bool = masks.astype(bool)

    # Compute pixel count per instance (vectorized)
    pixel_per_instance = masks_bool.sum(axis=(1, 2))  # shape (N,)

    # Aggregate per class
    for cls_id, pixel_count in zip(classes.astype(int), pixel_per_instance):
        display_name = CLASS_NAMES[int(cls_id)]
        area_by_class[display_name] += int(pixel_count)

    return area_by_class

def calculate_percentage(pixel_count):
    """
    Convert pixel counts to class-wise percentages.

    Args:
        pixel_count (dict): Mapping from class name to pixel count.

    Returns:
        dict: Mapping from class name to percentage of total pixels.
    """
    total = sum(pixel_count.values())
    return {
        k: (v / total * 100 if total > 0 else 0)
        for k, v in pixel_count.items()
    }
