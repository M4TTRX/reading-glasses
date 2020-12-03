from pytesseract import pytesseract, get_tesseract_version, image_to_string
import cv2
import time
from tabulate import tabulate


def get_image_time(img):
    # start timer
    start = time.time()

    # run tesseract
    image_to_string(img)

    # measure end time and return duration
    end = time.time()
    return end - start


def benchmark_img(img, iter=1000):
    times = [get_image_time(img) for _ in range(iter)]
    return [
        sum(times) / len(times),
        min(times),
        max(times),
    ]


if __name__ == "__main__":

    # set up paths
    tesseract_path = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    pytesseract.tesseract_cmd = tesseract_path

    # import images
    img_path = "experimentation/res/performance/"
    pargraph_img = cv2.imread(img_path + "paragraph.jpg", 1)
    line_img = cv2.imread(img_path + "line.jpg", 1)
    word_img = cv2.imread(img_path + "word_announced.jpg", 1)

    # benchmark performance between images
    paragraph_benchmark = ["Paragraph"] + benchmark_img(pargraph_img, iter=100)
    line_benchmark = ["Line"] + benchmark_img(line_img, iter=100)
    word_benchmark = ["Word"] + benchmark_img(word_img, iter=100)

    # print results
    print(
        tabulate(
            [paragraph_benchmark, line_benchmark, word_benchmark],
            headers=["Type", "Average", "Min", "Max"],
        )
    )
