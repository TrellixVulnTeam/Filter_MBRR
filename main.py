import numpy as np
import cv2
import matplotlib.pyplot as plt


a = np.array([[[430, 386, 54]]])
print(len(a))
a = np.append(a, [[[480, 386, 54]]], axis=1)
print(a)
print("")


img = cv2.imread('k1.jpg')
for i in a[0, :]:
    print(i)
    cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 4)
    cv2.circle(img, (i[0], i[1]), 2, (255, 0, 0), 7)

plt.imshow(img)
plt.show()