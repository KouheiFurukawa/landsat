import matplotlib.pyplot as plt
import cv2
from pylab import *

W = 4096
H = 4096
# xi = 13500 - W // 2
# yi = 16500 - H // 2
xi = 8000 - W // 2
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

im3 = np.minimum(np.abs((im1 - im2) * 30), roof)
im3 = np.array(im3, dtype=uint8)
im1 = np.array(im1, dtype=uint8)
im2 = np.array(im2, dtype=uint8)
figure(3)
plt.imshow(roof - im3)

im4 = np.zeros((W, H), dtype=uint8)

result = cv2.merge((im1, im3, im1))
figure(4)
plt.imshow(result)

plt.show()
