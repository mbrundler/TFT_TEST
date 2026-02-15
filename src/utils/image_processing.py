"""Image processing utilities for screen analysis"""

import cv2
import numpy as np
from typing import Tuple, List, Optional


def preprocess_for_ocr(image: np.ndarray) -> np.ndarray:
    """
    Preprocess image for better OCR accuracy

    Args:
        image: BGR image array

    Returns:
        Preprocessed grayscale image
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    processed = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

    return processed


def find_template(
    image: np.ndarray,
    template: np.ndarray,
    threshold: float = 0.8
) -> Optional[Tuple[int, int]]:
    """
    Find template in image using template matching

    Args:
        image: Source image to search in
        template: Template image to find
        threshold: Matching threshold (0-1)

    Returns:
        (x, y) coordinates of match or None
    """
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        return max_loc

    return None


def extract_region(
    image: np.ndarray,
    x: int,
    y: int,
    width: int,
    height: int
) -> np.ndarray:
    """
    Extract rectangular region from image

    Args:
        image: Source image
        x: X coordinate of top-left corner
        y: Y coordinate of top-left corner
        width: Region width
        height: Region height

    Returns:
        Extracted region
    """
    return image[y:y+height, x:x+width]


def detect_color_region(
    image: np.ndarray,
    color_lower: Tuple[int, int, int],
    color_upper: Tuple[int, int, int]
) -> List[Tuple[int, int, int, int]]:
    """
    Detect regions of specific color in image

    Args:
        image: BGR image
        color_lower: Lower bound of color range (B, G, R)
        color_upper: Upper bound of color range (B, G, R)

    Returns:
        List of bounding boxes (x, y, w, h)
    """
    # Create mask for color range
    mask = cv2.inRange(image, np.array(color_lower), np.array(color_upper))

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get bounding boxes
    boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        boxes.append((x, y, w, h))

    return boxes


def resize_for_analysis(
    image: np.ndarray,
    target_width: int = 1920
) -> np.ndarray:
    """
    Resize image to standard width for consistent analysis

    Args:
        image: Input image
        target_width: Target width in pixels

    Returns:
        Resized image
    """
    height, width = image.shape[:2]
    aspect_ratio = height / width
    target_height = int(target_width * aspect_ratio)

    return cv2.resize(image, (target_width, target_height))


def enhance_contrast(image: np.ndarray) -> np.ndarray:
    """
    Enhance image contrast for better detection

    Args:
        image: Input image

    Returns:
        Enhanced image
    """
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)

    enhanced = cv2.merge([l, a, b])
    return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
