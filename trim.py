import matplotlib.pyplot as plt
import cv2
from pylab import figure
import numpy as np

filename = 'PRD_RGB_20180708_004_0000208911.tif'
W = 40
H = 40
# xi = 13500 - W // 2
# yi = 16500 - H // 2
xi = 7450 - W // 2
yi = 14230 - H // 2

im = cv2.imread(filename)
im = im[yi:yi + W, xi:xi + H, 2]
figure(1)
plt.imshow(im, cmap='gray')
# cv2.imwrite('taorekomi.png', im)
plt.colorbar()
plt.show()
