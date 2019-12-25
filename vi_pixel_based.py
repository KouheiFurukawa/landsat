import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
from pylab import *
from inspect import signature

from lee_filter_c import lee_sigma
from module_change_detection import *

W = 4000
H = 4000
# xi = 13500 - W // 2
# yi = 16500 - H // 2
xi = 8000 - W // 2
yi = 14500 - H // 2

bins = 256

filename = "PRD_RGB_20180708_004_0000208911.tif"

im = cv2.imread(filename)

im1 = im[yi:yi + W, xi:xi + H, 2]  # extract subimage
figure(1)
plt.imshow(im1, cmap="gray")

im2 = im[yi:yi + W, xi:xi + H, 0]  # extract subimage
figure(2)
plt.imshow(im2, cmap="gray")

p1 = get_p_map(im1, W)
p2 = get_p_map(im2, W)
p12 = get_p_map_2d(im1, im2, W)

g = cv2.imread('ground_truth_mabi.tif')
ans = g[2000 - W // 2:2000 + W // 2, 2000 - W // 2:2000 + W // 2, 0]
figure(3)
plt.imshow(ans)

result = mixed_information(0.151, im1, im2, W)
figure(4)
plt.imshow(result)

output = thresholding(result, W)
output2 = cv2.merge((output, im1, im2))
figure(5)
plt.imshow(output2)
plt.show()


a_list = [0.04 * i for i in range(25)]
recall = []
precision = []
for alpha in a_list:
    pr = clustering(p1, p2, p12, alpha, W, ans)
    print(pr)
    recall.append(pr[1])
    precision.append(pr[0])
precision.append(1)
recall.append(0)
figure(6)
plt.scatter(recall, precision)
