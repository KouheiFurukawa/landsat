import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
from pylab import *
np.set_printoptions(threshold=np.inf)

W = 9
H = 9
# xi = 13500 - W // 2
# yi = 16500 - H // 2
xi = 8500 - W // 2
yi = 14500 - H // 2

bins = 64

win = 3

filename = "PRD_RGB_20180708_004_0000208911.tif"

im = cv2.imread(filename)  # -1 for 16bit image

im1 = im[yi:yi + W, xi:xi + H, 2]  # extract subimage
figure(1)
plt.imshow(im1)

im2 = im[yi:yi + W, xi:xi + H, 0]  # extract subimage
figure(2)
plt.imshow(im2)

im1_flat = im1.flatten()
im2_flat = im2.flatten()


def kullback_leibler(i1, i2):
    h1 = np.histogram(i1, bins=np.linspace(0, 256, bins + 1))[0]
    h2 = np.histogram(i2, bins=np.linspace(0, 256, bins + 1))[0]

    h1 = h1 / (win * win)
    h2 = h2 / (win * win)

    print(h1)
    print(h2)
    output = 0
    for i in range(bins):
        if h2[i] != 0 and h1[i] != 0:
            output += h1[i] * math.log((h1[i] / h2[i]), 2)

    return output


result = np.zeros((W - win + 1, H - win + 1), dtype=np.uint8)
margin = (win - 1) // 2

for k in range(margin, W - margin):
    for l in range(margin, H - margin):
        win1 = im1[k - margin:k + margin + 1, l - margin:l + margin + 1]
        win2 = im2[k - margin:k + margin + 1, l - margin:l + margin + 1]
        win1_flat = win1.flatten()
        win2_flat = win2.flatten()
        result[k - margin][l - margin] = kullback_leibler(win1_flat, win2_flat) + kullback_leibler(win2_flat, win1_flat)

figure(3)
plt.imshow(result)

n = np.max(result)
print(np.max(result))
print(np.min(result))

result2 = np.zeros((W - win + 1, H - win + 1), dtype=np.uint8)
for u in range(W - win + 1):
    for v in range(H - win + 1):
        result2[u][v] = math.floor(result[u][v] * 255 / n)

im1 = im1[margin:W - margin, margin:H - margin]
result_overlay = cv2.merge((result2, im1, im1))
figure(4)
plt.imshow(result_overlay)

plt.show()
