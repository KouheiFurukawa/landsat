import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
from pylab import *

np.set_printoptions(threshold=np.inf)

W = 1000
H = 1000
# xi = 13500 - W // 2
# yi = 16500 - H // 2
xi = 8500 - W // 2
yi = 14500 - H // 2

bins = 256

filename = "PRD_RGB_20180708_004_0000208911.tif"

im = cv2.imread(filename)

im1 = im[yi:yi + W, xi:xi + H, 2]  # extract subimage
figure(1)
plt.imshow(im1)

im2 = im[yi:yi + W, xi:xi + H, 0]  # extract subimage
figure(2)
plt.imshow(im2)

im1_flat = im1.flatten()
im2_flat = im2.flatten()

hst1 = np.histogram(im1_flat, bins=np.linspace(0, 256, bins + 1))[0]
hst2 = np.histogram(im2_flat, bins=np.linspace(0, 256, bins + 1))[0]
hst12 = np.histogram2d(im1_flat, im2_flat, bins=[np.linspace(0, 256, bins + 1), np.linspace(0, 256, bins + 1)])[0]
hst1 = hst1 / (W * H)
hst2 = hst2 / (W * H)
hst12 = hst12 / (W * H)

result = np.zeros((W, H), dtype=float)
result1d = []
for k in range(W):
    for l in range(H):
        p1 = hst1[im1[k][l]]
        p2 = hst2[im2[k][l]]
        p12 = hst12[im1[k][l]][im2[k][l]]

        if p1 > 0 and p2 > 0 and p12 > 0:
            result[k][l] = math.log(p12 / (p1 * p2), 2)
            result1d.append((result[k][l], k, l))

mi_sum = sum([x[0] for x in result1d])
result1d.sort(key=lambda x: x[0], reverse=True)
mi_half_sum = 0
changed = []

for i in range(len(result1d)):
    if result1d[i][0] > 0:
        mi_half_sum += result1d[i][0]
        changed.append((result1d[i][1], result1d[i][2]))

result_threshold = np.full((W, H), 255, dtype=uint8)

for c in changed:
    result_threshold[c[0]][c[1]] = 0

r = max(np.max(result), -np.min(result))
result /= r
figure(3)
plt.imshow(result)

figure(4)
plt.imshow(result_threshold)

output = cv2.merge((result_threshold, im1, im1))
figure(5)
plt.imshow(output)

plt.show()
