import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
from pylab import *
from lee_filter import *
from module_change_detection import *

np.set_printoptions(threshold=np.inf)

W = 4000
H = 4000
# xi = 13500 - W // 2
# yi = 16500 - H // 2
xi = 8000 - W // 2
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

hist_map_1 = get_p_map(im1, W)
hist_map_2 = get_p_map(im2, W)
hist_map_12 = get_p_map_2d(im1, im2, W)
print(hist_map_1[0][0])
print(hist_map_2[0][0])
print(hist_map_12[0][0])

g = cv2.imread('ground_truth_mabi.tif')
ans = g[2000 - W // 2:2000 + W // 2, 2000 - W // 2:2000 + W // 2, 0]
ans = ground_truth(ans, W)
figure(3)
plt.imshow(ans)

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
print(alpha)

result = np.zeros((W, H), dtype=np.float)
for k in range(H):
    for l in range(W):
        p1 = hst1[im1[k][l]]
        p2 = hst2[im2[k][l]]
        p12 = hst12[im1[k][l]][im2[k][l]]
        result[k][l] = (1 + alpha) * math.log(p12, 2) - math.log(p1 * p2, 2)

# figure(4)
# result = cv2.merge((result, im1, im2))
# plt.imshow(result)
tp = 0
fp = 0
fn = 0
tn = 0
output = np.zeros((W, H), dtype=np.uint8)

for k in range(H):
    for l in range(W):
        if result[k][l] < 0 and int(im1[k][l]) - int(im2[k][l]) > 3:
            output[k][l] = 255
            if ans[k][l] == 1:
                tp += 1
            else:
                fp += 1
        else:
            if ans[k][l] == 1:
                fn += 1
            else:
                tn += 1

output = cv2.merge((output, im1, im2))
figure(5)
plt.imshow(output)

# print(tp, fp, fn, tn)
# print('recall', tp / (tp + fn))
# print('precision', tp / (tp + fp))
# print(clustering_new(im1, im2, hist_map_1, hist_map_2, hist_map_12, alpha, W, ans))
plt.show()
