import numpy as np
import matplotlib.pyplot as plt
import cv2
from pylab import *

W = 4096
H = 4096
xi = 13500 - W // 2
yi = 16500 - H // 2
# xi = 8000 - W // 2
# yi = 14500 - H // 2
bins = 256

win = 16

filename = "PRD_RGB_20180708_004_0000208911.tif"

im = cv2.imread(filename, -1)  # -1 for 16bit image


im1 = im[yi:yi + W, xi:xi + H, 2]  # extract subimage
figure(1)
im4 = np.zeros((W, H), dtype=uint8)
plt.imshow(cv2.merge((im1, im1, im4)))

im2 = im[yi:yi + W, xi:xi + H, 0]  # extract subimage
figure(2)
plt.imshow(im2)

result = np.zeros((W, H), dtype=np.uint8)

for k in range(W // win):
    for l in range(H // win):
        win1 = im[yi + k * win:yi + (k + 1) * win, xi + l * win:xi + (l + 1) * win, 2]
        win2 = im[yi + k * win:yi + (k + 1) * win, xi + l * win:xi + (l + 1) * win, 0]
        win1_flat = win1.flatten()
        win2_flat = win2.flatten()
        x = np.array([win1_flat, win2_flat])
        cc = np.corrcoef(x)
        result[k * win:(k + 1) * win, l * win:(l + 1) * win] = 255 - max(int(255 * cc[0][1]), 0)


figure(3)
plt.imshow(result)
result2 = cv2.merge((im1, result, im1))
figure(5)
plt.imshow(result2)

plt.show()
