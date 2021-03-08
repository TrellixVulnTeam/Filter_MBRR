import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('ser.jpg')
pixels = img.copy()
x, y, c = pixels.shape

pixels = cv2.cvtColor(pixels, cv2.COLOR_RGB2GRAY)
s = 0
for j in range(y):
	for i in range(x):
		s = pixels[i, j]
		if 255 - s <= s:
			p = 255 - s
			p = -p
			pixels[i, j] = 255
		else:
			p = s
			pixels[i, j] = 0

		if i != x - 1:
			k = pixels[i + 1, j]
			k = k + ((p * 7) // 16)
			if k > 255:
				k = 255
			elif k < 0:
				k = 0
			pixels[i + 1, j] = k

		if j != y - 1:
			k = pixels[i, j + 1]
			k = k + ((p * 5) // 16)
			if k > 255:
				k = 255
			elif k < 0:
				k = 0
			pixels[i, j + 1] = k

		if j != y - 1 and i != x - 1:
			k = pixels[i + 1, j + 1]
			k = k + (p // 16)
			if k > 255:
				k = 255
			elif k < 0:
				k = 0
			pixels[i + 1, j + 1] = k

		if j != y - 1 and i != 0:
			k = pixels[i - 1, j + 1]
			k = k + ((p * 3) // 16)
			if k > 255:
				k = 255
			elif k < 0:
				k = 0
			pixels[i - 1, j + 1] = k
cv2.imshow('Grayscale', pixels)

cv2.waitKey(0)