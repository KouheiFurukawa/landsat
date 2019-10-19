import matplotlib.pyplot as plt
import cv2
from pylab import *

W = 4000
H = 4000
# xi = 13500 - W // 2
# yi = 16500 - H // 2
xi = 8500 - W // 2
yi = 14500 - H // 2
bins = 256

win = 32

filename = "PRD_RGB_20180708_004_0000208911.tif"

im = cv2.imread(filename, -1)  # -1 for 16bit image


im1 = np.array(im[yi:yi + W, xi:xi + H, 2], dtype=int8)  # extract subimage
figure(1)
plt.imshow(im1)

im2 = np.array(im[yi:yi + W, xi:xi + H, 0], dtype=int8)  # extract subimage
figure(2)
plt.imshow(im2)

roof = np.full((W, H), 255, dtype=uint8)

figure(5)
im3 = np.array(im[yi:yi + W, xi:xi + H, 2], dtype=int8)
for k in range(W):
    for l in range(H):
        im3[k][l] = abs(im2[k][l] - im1[k][l])
im3 = im3.flatten()
print(im3)
plt.hist(im3, bins=51, range=(0, 50))

im1 = np.array(im1, dtype=uint8)
im2 = np.array(im2, dtype=uint8)

plt.show()
