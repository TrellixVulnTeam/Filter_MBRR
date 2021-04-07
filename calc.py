import numpy as np
import cv2
import matplotlib.pyplot as plt


a = np.array([[[3, 4, 5], [3, 4, 5]]])
a = np.delete(a, 0, axis=1)
print(a)
print("")