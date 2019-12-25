import matplotlib.pyplot as plt
import cv2
from pylab import figure
import numpy as np

filename = 'ground_truth.tif'
W = 4000
H = 4000
# xi = 13500 - W // 2
# yi = 16500 - H // 2
xi = 8000 - W // 2
yi = 14500 - H // 2

im = cv2.imread(filename)
im = im[yi:yi + W, xi:xi + H]
figure(1)
plt.imshow(im)

result = np.zeros((W, H), dtype=np.uint8)
for i in range(H):
    for j in range(W):
        if im[i][j][0] > 0 or im[i][j][1] > 0 or im[i][j][2] > 0:
            result[i][j] = 255

figure(2)
plt.imshow(result)

cv2.imwrite('ground_truth_mabi.tif', result)

plt.show()
