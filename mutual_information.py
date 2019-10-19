import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
from pylab import *
from sklearn.cluster import KMeans
np.set_printoptions(threshold=np.inf)

W = 1000
H = 1000
# xi = 13500 - W // 2
# yi = 16500 - H // 2
xi = 8500 - W // 2
yi = 14500 - H // 2

bins = 64

win = 7

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


def pixel(x, h):
    h_norm = h[0] / 256
    return h_norm[x]


def entropy(img):
    hst = np.histogram(img, bins=np.linspace(0, 256, bins + 1))
    output = 0
    for x in range(bins):
        pp = pixel(x, hst)
        if pp != 0:
            output -= math.log(pp, 2) * pp
    return output


def pixel2d(x, y, h):
    h_norm = h[0] / 256
    return h_norm[x][y]


def mutual_entropy(i1, i2):
    hst = np.histogram2d(i1, i2, bins=[np.linspace(0, 256, bins + 1), np.linspace(0, 256, bins + 1)])
    output = 0
    for i in range(bins):
        for j in range(bins):
            pp = pixel2d(i, j, hst)
            if pp != 0:
                output -= math.log(pp, 2) * pp
    return output


result = np.zeros((W - win + 1, H - win + 1), dtype=np.uint8)
margin = (win - 1) // 2

for k in range(margin, W - margin):
    for l in range(margin, H - margin):
        win1 = im1[k - margin:k + margin + 1, l - margin:l + margin + 1]
        win2 = im2[k - margin:k + margin + 1, l - margin:l + margin + 1]
        win1_flat = win1.flatten()
        win2_flat = win2.flatten()
        entropy_sum = entropy(win1_flat) + entropy(win2_flat)
        if entropy_sum == 0:
            mi_norm = 1
        else:
            mi = entropy_sum - mutual_entropy(win1_flat, win2_flat)
            mi_norm = (2 * mi) / entropy_sum
        result[k - margin, l - margin] = 255 - math.floor(mi_norm * 255)

result_flat = result.flatten()
result_flat = result_flat.reshape([-1, 1])

pred = KMeans(n_clusters=2).fit_predict(result_flat)
pred = pred.reshape([W - win + 1, H - win + 1])

ave_0 = np.mean([result[x][y] for x in range(H - win + 1) for y in range(W - win + 1) if pred[x][y] == 0])
ave_1 = np.mean([result[x][y] for x in range(H - win + 1) for y in range(W - win + 1) if pred[x][y] == 1])

ave = [(ave_0, 0), (ave_1, 1)]
ave.sort(key=lambda x: x[0])

output = np.zeros((W - win + 1, H - win + 1), dtype=np.uint8)
for k in range(W - win + 1):
    for l in range(H - win + 1):
        if pred[k][l] == ave[0][1]:
            output[k][l] = 255
        elif pred[k][l] == ave[1][1]:
            output[k][l] = 0

figure(3)
im1 = im1[margin:W - margin, margin:H - margin]
output = cv2.merge((output, im1, im1))
plt.imshow(output)
#
# figure('im1: 100%, result: 100%')
# result3 = cv2.merge((result, im1, im1))
# plt.imshow(result3)
#
# im1 *= 2
# result *= 2
# figure('im1: 200%, result: 200%')
# result4 = cv2.merge((result, im1, im1))
# plt.imshow(result4)
#
# im1 //= 2
# result2 = cv2.merge((result, im1, im1))
# figure('im1: 100%, result: 200%')
# plt.imshow(result2)
#
# im1 //= 2
# result5 = cv2.merge((result, im1, im1))
# figure('im1: 50%, result: 200%')
# plt.imshow(result5)
plt.show()
