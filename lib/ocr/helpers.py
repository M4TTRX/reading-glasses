from time import localtime
from cv2 import (
    resize,
    INTER_AREA,
    minAreaRect,
    getRotationMatrix2D,
    warpAffine,
    INTER_CUBIC,
    BORDER_REPLICATE,
)
from numpy import column_stack, where


def resize_img(img, max_side=1000):
    """
    This function resizes an image, while keeping its aspect ratio,
    ensuring that its largest side is not greater
    than max_side (1000px by default).
    """
    height, width = img.shape
    # if the image is small enough as is, return it unchanged
    if height <= 1000 and width <= 1000:
        return img
    dim = tuple()
    if height > width:
        scale_ratio = max_side / height
        dim = (int(width * scale_ratio), max_side)
    else:
        scale_ratio = max_side / width
        dim = (max_side, int(height * scale_ratio))
    return resize(img, dim, interpolation=INTER_AREA)


# this function deskews an image
def deskew(image):
    coords = column_stack(where(image > 0))
    angle = minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = getRotationMatrix2D(center, angle, 1.0)
    rotated = warpAffine(
        image, M, (w, h), flags=INTER_CUBIC, borderMode=BORDER_REPLICATE
    )
    return rotated