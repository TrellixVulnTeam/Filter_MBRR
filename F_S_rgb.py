import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('k1.jpg')
pixels = img.copy()
x, y, c = pixels.shape
print(x, y)
s = 0
for j in range(y):
    for i in range(x):
        r, g, b = pixels[i, j]
        if r >= g and r >= b:
            p = 255 - r
            if p < 0:
                p = 0
            pixels[i, j] = 255, 0, 0

            if j != y - 1:
                r, g, b = pixels[i, j + 1]
                r = r - ((p * 5) // 16)
                g = g + ((p * 5) // 16)
                b = b + ((p * 5) // 16)
                pixels[i, j + 1] = r, g, b

            if j > y - 1 and i > x - 1:
                r, g, b = pixels[i + 1, j + 1]
                r = r - (p // 16)
                g = g + (p // 16)
                b = b + (p // 16)
                pixels[i + 1, j + 1] = r, g, b

            if j != y - 1 and i != 0:
                r, g, b = pixels[i - 1, j + 1]
                r = r - ((p * 3) // 16)
                g = g + ((p * 3) // 16)
                b = b + ((p * 3) // 16)
                pixels[i - 1, j + 1] = r, g, b

            if i != x - 1:
                r, g, b = pixels[i + 1, j]
                r = r - ((p * 7) // 16)
                g = g + ((p * 7) // 16)
                b = b + ((p * 7) // 16)
                pixels[i + 1, j] = r, g, b

        elif g >= r and g >= b:
            p = 255 - g
            if p < 0:
                p = 0
            pixels[i, j] = 0, 255, 0

            if j != y - 1:
                r, g, b = pixels[i, j + 1]
                r = r + ((p * 5) // 16)
                g = g - ((p * 5) // 16)
                b = b + ((p * 5) // 16)
                pixels[i, j + 1] = r, g, b

            if j != y - 1 and i != x - 1:
                r, g, b = pixels[i + 1, j + 1]
                r = r + (p // 16)
                g = g - (p // 16)
                b = b + (p // 16)
                pixels[i + 1, j + 1] = r, g, b

            if j != y - 1 and i != 0:
                r, g, b = pixels[i - 1, j + 1]
                r = r + ((p * 3) // 16)
                g = g - ((p * 3) // 16)
                b = b + ((p * 3) // 16)
                pixels[i - 1, j + 1] = r, g, b

            if i != x - 1:
                r, g, b = pixels[i + 1, j]
                r = r + ((p * 7) // 16)
                g = g - ((p * 7) // 16)
                b = b + ((p * 7) // 16)
                pixels[i + 1, j] = r, g, b

        else:
            p = 255 - b
            if p < 0:
                p = 0
            pixels[i, j] = 0, 0, 255

            if j != y - 1:
                r, g, b = pixels[i, j + 1]
                r = r + ((p * 5) // 16)
                g = g + ((p * 5) // 16)
                b = b - ((p * 5) // 16)
                pixels[i, j + 1] = r, g, b

            if j != y - 1 and i != x - 1:
                r, g, b = pixels[i + 1, j + 1]
                r = r + (p // 16)
                g = g + (p // 16)
                b = b - (p // 16)
                pixels[i + 1, j + 1] = r, g, b

            if j != y - 1 and i != 0:
                r, g, b = pixels[i - 1, j + 1]
                r = r + ((p * 3) // 16)
                g = g + ((p * 3) // 16)
                b = b - ((p * 3) // 16)
                pixels[i - 1, j + 1] = r, g, b

            if i != x - 1:
                r, g, b = pixels[i + 1, j]
                r = r + ((p * 7) // 16)
                g = g + ((p * 7) // 16)
                b = b - ((p * 7) // 16)
                pixels[i + 1, j] = r, g, b

status = cv2.imwrite('C:/Users/ivio0/Desktop/Filter/xz.jpg', pixels)
if status:
    print("Изображение сохранено")
cv2.imshow('Grayscale', pixels)
cv2.waitKey(0)