import cv2
import numpy as np
import matplotlib.pyplot as plt


def coindetect(img, p1, p2):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.GaussianBlur(img, (29, 29), cv2.BORDER_DEFAULT)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.45, 90, param1=p1, param2=p2, minRadius=10, maxRadius=400)
    circles_r = []
    if circles is not None:
        circles_r = np.uint16(np.around(circles))

    return circles_r
