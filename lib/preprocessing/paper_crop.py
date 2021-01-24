import cv2
import imutils
import numpy as np
from .four_point_transform import four_point_transform
from skimage.filters import threshold_local


def crop_paper(img, show_imgs=False, edge_crop_percentage=2):
    ratio = img.shape[0] / 500.0
    orig = img.copy()
    image = imutils.resize(img, height=500)
    edged = cv2.Canny(image, 75, 200)

    # show the original image and the edge detected image
    if show_imgs:
        cv2.imshow("Image", image)
        cv2.imshow("Edged", edged)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    cnts = cv2.findContours(
        edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
    )
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
        if len(approx) == 4:
            screenCnt = approx
            break

    # show the contour (outline) of the piece of paper
    if show_imgs:
        cv2.imshow("Outline", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # apply the four point transform to obtain a top-down
    # view of the original image
    try:
        warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    except:
        print("Image is already scanned properly")
        warped = orig
    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    T = threshold_local(warped, block_size=11, offset=5, method="gaussian")
    warped = (warped > T).astype("uint8") * 255

    # show the original and scanned images
    if show_imgs:
        cv2.imshow("Original", imutils.resize(orig, height=650))
        cv2.imshow("Scanned", imutils.resize(warped, height=650))
        cv2.waitKey(0)

    # crop image for no bleeding on edges
    w, h = warped.shape
    crop_pixel_width = int(edge_crop_percentage / 100 * w)
    crop_pixel_height = int(edge_crop_percentage / 100 * h)

    return warped[
        crop_pixel_height : h - crop_pixel_height,
        crop_pixel_width : w - crop_pixel_width,
    ]


def find_lines(img, show_imgs=False):
    ratio = img.shape[0] / 500.0
    orig = img.copy()
    img = imutils.resize(img, height=500)
    # threshold the grayscale image
    thresh = cv2.threshold(
        img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )[1]
    height, width = img.shape

    blur = cv2.blur(thresh, (3, 3))
    # use morphology erode to blur horizontally
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (151, 3))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)

    # Show progress if needed
    if show_imgs:
        cv2.imshow("THRESH", thresh)
        cv2.imshow("BLUR", blur)
        cv2.imshow("MORPH", morph)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # now that we have lines divided in big chonks of white
    # we can split the image in those

    # turn the image into an array that tells us whether there is a bloc or not
    row_values = [sum(row) for row in morph]

    # find the list of blocks by storing their index
    block_list = []
    block = []
    for i in range(len(row_values)):
        if len(block) == 0 and row_values[i] > 0:
            block.append(i)
        if len(block) == 1 and row_values[i] == 0:
            block.append(i)
            block_list.append(block)
            block = []
    # if no block were found add one big block
    if len(block) == 1:
        block.append(len(row_values))
        block_list.append(block)

    row_list = [
        orig[int(block[0] * ratio) : int(block[1] * ratio)]
        for block in block_list
    ]
    if show_imgs:
        for row in row_list:
            cv2.imshow("block", row)
            cv2.waitKey(0)
    return row_list


def get_lines_from_img(img, display_img=False):
    # convert inmage to grey if needed
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # crop out the paper
    cropped = crop_paper(img, show_imgs=display_img)

    # get the lines
    lines = find_lines(cropped, show_imgs=display_img)

    return lines


# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
images = [
    cv2.imread(f"lib/camera/img_saves/{i}.jpg", 1) for i in range(1, 4 + 1)
]
image = cv2.imread("lib/camera/img_saves/5.jpg", 1)
