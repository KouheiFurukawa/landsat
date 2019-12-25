import numpy as np
import matplotlib.pyplot as plt
import cv2
import pylab
from sklearn import linear_model

W = 4000
H = 4000
xi = 8000 - W // 2
yi = 14500 - H // 2
win = 5
margin = (win - 1) // 2

filename = "PRD_RGB_20180708_004_0000208911.tif"
im = cv2.imread(filename)

im1 = im[yi:yi + W, xi:xi + H, 2]  # extract subimage
pylab.figure(1)
plt.imshow(im1, cmap="gray")

im2 = im[yi:yi + W, xi:xi + H, 0]  # extract subimage
pylab.figure(2)
plt.imshow(im2, cmap="gray")

result_ave1 = []
result_std1 = []
result_ave2 = []
result_std2 = []

for k in range(W // win):
    for l in range(H // win):
        win1 = im1[k * win:(k + 1) * win, l * win:(l + 1) * win]
        win1_flat = win1.flatten()
        win2 = im2[k * win:(k + 1) * win, l * win:(l + 1) * win]
        win2_flat = win2.flatten()
        result_ave1.append(np.average(win1_flat))
        result_std1.append(np.std(win1_flat))
        result_ave2.append(np.average(win2_flat))
        result_std2.append(np.std(win2_flat))

clf = linear_model.LinearRegression()
print(np.average(result_ave2) - np.average(result_ave1))
result_ave1 = [[r] for r in result_ave1]
result_ave2 = [[r] for r in result_ave2]

clf.fit(result_ave1, result_std1)
c1 = clf.coef_

clf.fit(result_ave2, result_std2)
c2 = clf.coef_
plt.show()

print(c1, c2)
print(((c1 * np.average(result_ave1)) ** 2 + (c2 * np.average(result_ave2)) ** 2) ** 0.5)
