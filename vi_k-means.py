import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
from pylab import *
from lee_filter import *
from sklearn.cluster import KMeans

np.set_printoptions(threshold=np.inf)

W = 1000
H = 1000
# xi = 13500 - W // 2
# yi = 16500 - H // 2
xi = 8500 - W // 2
yi = 14500 - H // 2

# ノイズ検証用
# W = 512
# H = 512
# xi = 15500 - W // 2
# yi = 16200 - H // 2

bins = 256

filename = "PRD_RGB_20180708_004_0000208911.tif"

im = cv2.imread(filename)

im1 = im[yi:yi + W, xi:xi + H, 2]  # extract subimage
figure(1)
plt.imshow(im1, cmap="gray")

im2 = im[yi:yi + W, xi:xi + H, 0]  # extract subimage
figure(2)
plt.imshow(im2, cmap="gray")

im1_flat = im1.flatten()
im2_flat = im2.flatten()

hst1 = np.histogram(im1_flat, bins=np.linspace(0, 256, bins + 1))[0]
hst2 = np.histogram(im2_flat, bins=np.linspace(0, 256, bins + 1))[0]
hst12 = np.histogram2d(im1_flat, im2_flat, bins=[np.linspace(0, 256, bins + 1), np.linspace(0, 256, bins + 1)])[0]
hst1 = hst1 / (W * H)
hst2 = hst2 / (W * H)
hst12 = hst12 / (W * H)

mi = 0
for i in range(256):
    for j in range(256):
        if hst1[i] > 0 and hst2[j] > 0 and hst12[i][j] > 0:
            mi += hst12[i][j] * math.log(hst12[i][j] / (hst1[i] * hst2[j]), 2)

vi = 0
for i in range(256):
    for j in range(256):
        if hst1[i] > 0 and hst2[j] > 0 and hst12[i][j] > 0:
            vi -= hst12[i][j] * math.log((hst12[i][j] ** 2) / (hst1[i] * hst2[j]), 2)

alpha = mi / (vi + mi)

result = np.zeros((W, H), dtype=np.float)
for k in range(W):
    for l in range(H):
        p1 = hst1[im1[k][l]]
        p2 = hst2[im2[k][l]]
        p12 = hst12[im1[k][l]][im2[k][l]]
        result[k][l] = (1 + alpha) * math.log(p12, 2) - math.log(p1 * p2, 2)

result_flat = result.flatten()
result_flat = result_flat.reshape([-1, 1])
pred = KMeans(n_clusters=2).fit_predict(result_flat)
pred = pred.reshape([W, H])

ave_0 = np.mean([result[x][y] for x in range(H) for y in range(W) if pred[x][y] == 0])
ave_1 = np.mean([result[x][y] for x in range(H) for y in range(W) if pred[x][y] == 1])

ave = [(ave_0, 0), (ave_1, 1)]
ave.sort(key=lambda x: x[0])

output = np.zeros((W, H), dtype=np.uint8)
for k in range(W):
    for l in range(H):
        if pred[k][l] == ave[0][1]:
            output[k][l] = 255
        elif pred[k][l] == ave[1][1]:
            output[k][l] = 0

output = cv2.merge((output, im1, im1))
figure(3)
plt.imshow(output)

plt.show()