import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
from pylab import *
import bisect
np.set_printoptions(threshold=np.inf)

W = 4096
H = 4096
xi = 13500 - W // 2
yi = 16500 - H // 2
# xi = 8000 - W // 2
# yi = 14500 - H // 2
# xi = 15048
# yi = 14564
bins = 256

win = 32

filename = "PRD_RGB_20180708_004_0000208911.tif"

im = cv2.imread(filename, -1)  # -1 for 16bit image

im1 = im[yi:yi + W, xi:xi + H, 2]  # extract subimage
figure(1)
plt.imshow(im1)

im2 = im[yi:yi + W, xi:xi + H, 0]  # extract subimage
figure(2)
plt.imshow(im2)

im1_flat = im1.flatten()
im2_flat = im2.flatten()


def pixel(x, h):
    return h[0][x]


def entropy(img):
    hst = np.histogram(img, bins=np.linspace(0, bins, bins + 1), normed=True)
    output = 0
    for x in img:
        pp = pixel(x, hst)
        if pp != 0:
            output -= math.log(pp, 2) * pp
    return output


def pixel2d(x, y, h):
    return h[0][x][y]


def mutual_entropy(i1, i2):
    hst = np.histogram2d(i1, i2, bins=np.linspace(0, bins, bins + 1), normed=True)
    output = 0
    for i in range(len(i1)):
        pp = pixel2d(i1[i], i2[i], hst)
        output -= math.log(pp, 2) * pp
    return output


result = np.zeros((W, H), dtype=np.uint8)

for k in range(W // win):
    for l in range(H // win):
        win1 = im[yi + k * win:yi + (k + 1) * win, xi + l * win:xi + (l + 1) * win, 2]
        win2 = im[yi + k * win:yi + (k + 1) * win, xi + l * win:xi + (l + 1) * win, 0]
        win1_flat = win1.flatten()
        win2_flat = win2.flatten()
        mi = min(2 * mutual_entropy(win1_flat, win2_flat) / (entropy(win1_flat) + entropy(win2_flat)), 1)
        result[k * win:(k + 1) * win, l * win:(l + 1) * win] = 255 - int(mi * 255)

figure(3)
plt.imshow(result)
result2 = cv2.merge((im1, result, im1))
figure(5)
plt.imshow(result2)

plt.show()
