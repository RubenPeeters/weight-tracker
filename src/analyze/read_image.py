import cv2 as cv


def read_image(path):
    return cv.imread(str(path))
