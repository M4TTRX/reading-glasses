from time import localtime
import cv2
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
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


# this function deskews an image
def deskew(image):
    coords = column_stack(where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image,
        M,
        (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE,
    )
    cv2.imshow("Edged", cv2.edged)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return rotated
