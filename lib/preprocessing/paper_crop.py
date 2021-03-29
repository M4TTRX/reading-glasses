import cv2
import imutils
import numpy as np
from .four_point_transform import four_point_transform
from skimage.filters import threshold_local


def crop_paper(img, show_imgs=False, edge_crop_percentage=2):
    # Keep a copy of the original image for later
    orig = img.copy()

    # Resize the image to something smaller for easier processing
    ratio = img.shape[0] / 500.0
    paper = imutils.resize(img, height=500)

    # Thresholding

    # Get a threshold by finding the most promimnon shade in the image, which
    # we assume is the paper
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    # discard dark values
    minval = 100
    hist = hist[minval:]
    threshold = np.argmax(hist) - 20 + minval

    ret, thresh_gray = cv2.threshold(paper, threshold, 255, cv2.THRESH_BINARY)

    # Show the original image and the edge detected image
    if show_imgs:
        cv2.imshow("Image", thresh_gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Find the contours in the edged image
    contours = cv2.findContours(
        thresh_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )[0]

    paper_contour = []
    max_area = 0

    for c in contours:
        # Turn the contours into polygons
        peri = cv2.arcLength(c, True)
        countour_poly = cv2.approxPolyDP(c, 0.02 * peri, True)

        # compute the area of the polygon
        area = cv2.contourArea(countour_poly)

        # Turn those polygons into boxes bounding those polygons. This is
        # needed as usually the polygon encompassing the paper isn't rectangular
        rect = cv2.minAreaRect(countour_poly)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # Draw the countours for potential debugging
        if show_imgs:
            cv2.drawContours(paper, [box], 0, (255, 255, 255), 2)
        if area > max_area:
            # we consider the bounding box encompassing the polygon with the
            # largest area to be the paper
            paper_contour = box

    # get bounding box of the paper contour

    # show the contour (outline) of the piece of paper
    if show_imgs:
        cv2.imshow("paper", paper)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # apply the four point transform to obtain a top-down
    # view of the original image
    try:
        warped = four_point_transform(
            orig, paper_contour.reshape(4, 2) * ratio
        )
    except:
        print("Image is already scanned properly")
        warped = orig

    # Threshold the image to give it that 'black and white' paper effect
    T = threshold_local(warped, block_size=11, offset=5, method="gaussian")
    warped = (warped > T).astype("uint8") * 255

    # Show the original and scanned images
    if show_imgs:
        cv2.imshow("Original", imutils.resize(orig, height=650))
        cv2.imshow("Scanned", imutils.resize(warped, height=650))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Crop image for no bleeding on edges
    w, h = warped.shape
    crop_pixel_width = int(edge_crop_percentage / 100 * w)
    crop_pixel_height = int(edge_crop_percentage / 100 * h)

    result_img = warped[
        crop_pixel_height : h - crop_pixel_height,
        crop_pixel_width : w - crop_pixel_width,
    ]

    # if debugging is on, save the image for proper viewing
    if show_imgs:
        cv2.imwrite("result_img.jpg", result_img)
    return result_img


def find_lines(img, show_imgs=False):
    # back up the original image
    orig = img.copy()

    # Resize the image to something smaller to make processing faster
    ratio = img.shape[0] / 500
    paper = imutils.resize(img, height=500)

    # Blur the image to turn sentences in words into one blurb of darker grey
    paper = cv2.GaussianBlur(paper, (5, 5), cv2.BORDER_DEFAULT)

    # Show progress if needed
    if show_imgs:
        cv2.imshow("Blurred Resized image", paper)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Thresholding

    # Get a threshold by finding the most promimnon shade of white in the image
    hist = cv2.calcHist([paper], [0], None, [256], [0, 256])
    threshold = np.argmax(hist) - 30

    # Use Binary threshold to threshold the image
    ret, thresh_gray = cv2.threshold(paper, threshold, 255, cv2.THRESH_BINARY)

    # By now we our chunks of grey (the text) should be completely black,
    # while the rest should be completely white. Display if needed
    if show_imgs:
        cv2.imshow("Blurred + Thresholded image", thresh_gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Sometimes the edges of the paper were not cropped out and this can skew
    # the line filtering algorithm, so we need to crop the image.

    # Here we crop 10% of the image on both right and left.
    img_width = len(thresh_gray[0])

    # get the 10 % that we want to crop on each side
    crop_size = int(0.1 * img_width)
    cropped_img = thresh_gray[:, crop_size : img_width - crop_size]

    # Display the cropped image if verbose
    if show_imgs:
        cv2.imshow("Cropped image", cropped_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Invert the image so that the white values become 0 and the black ones
    # (the text) become greater than 0
    inv_img = (
        cropped_img + 1
    )  # the values at 255 will wrap to 0, while the ones at 0 will become 1

    # Get the sum of values on each row of the image. If there is any text in
    # this row, the value will be greater than 0, else, it will be 0.

    row_values = [sum(row) for row in inv_img]

    # Find the list of paragraphs/lines by storing their index
    block_list = []
    block = []
    for i in range(len(row_values)):
        # If we are not selecting a block and we detect text start selecting
        # the block
        if len(block) == 0 and row_values[i] > 0:
            block.append(i)
        # If we are selecting a block and the next value is 0, the block is over
        # and we should add the block to the block list and empty it.
        if len(block) > 0 and row_values[i] == 0:
            block.append(i)
            block_list.append(block)
            block = []
    # If no block were found add one big block, this also closes the last block
    if len(block) == 1:
        block.append(len(row_values))
        block_list.append(block)

    row_list = [
        # Blurring removes artifacts in the full res image
        cv2.GaussianBlur(
            # Select the paragraphs in the original image using the list of
            # blocks we obtained
            orig[int(block[0] * ratio) : int(block[1] * ratio), :],
            (3, 3),
            cv2.BORDER_DEFAULT,
        )
        for block in block_list
    ]

    # Show all the blocks if needed
    if show_imgs:
        for row in row_list:
            cv2.imshow("block", row)
            cv2.waitKey(0)
        cv2.destroyAllWindows()
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
