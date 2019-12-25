import numpy as np
import matplotlib.pyplot as plt
import cv2
from pylab import *
from sklearn.metrics import precision_recall_curve, average_precision_score
from inspect import signature
from module_change_detection import *

W = 4004
H = 4004
# xi = 13500 - W // 2
# yi = 16500 - H // 2
xi = 8000 - W // 2
yi = 14500 - H // 2
bins = 256

win = 5
margin = (win - 1) // 2

filename = "PRD_RGB_20180708_004_0000208911.tif"

im = cv2.imread(filename, -1)  # -1 for 16bit image

im1 = im[yi:yi + W, xi:xi + H, 2]  # extract subimage
figure(1)
plt.imshow(im1)

im2 = im[yi:yi + W, xi:xi + H, 0]  # extract subimage
figure(2)
plt.imshow(im2)

result = correlation_c(im1, im2, win, W)

plt.figure(8)
im3_flat = result.flatten()
plt.hist(im3_flat, bins=51, range=(-1, 1))

W -= win - 1
H -= win - 1
im1 = im[yi:yi + W, xi:xi + H, 2]
im2 = im[yi:yi + W, xi:xi + H, 0]

figure(3)
plt.imshow(result)

g = cv2.imread('ground_truth_mabi.tif')
ans = g[2000 - W // 2:2000 + W // 2, 2000 - W // 2:2000 + W // 2, 0]
figure(8)
ans = ground_truth(ans, W)
plt.imshow(ans)
ans_flat = ans.flatten()

# cv2.imwrite('corr_map.tif', result)
# cv2.imwrite('corr_map_th.png', result2)

figure(7)
im3_flat = result.flatten()

output = np.zeros((W, H), dtype=np.uint8)
for i in range(H):
    for j in range(W):
        if result[i][j] > -0.4:
            output[i][j] = 255

output = cv2.merge((output, im1, im2))
figure(4)
plt.imshow(output)

figure(5)
precision, recall, thresholds = precision_recall_curve(ans_flat, im3_flat)
print('precision:')
print(precision)
print('recall')
print(recall)
print('threshold')
print(thresholds)
step_kwargs = ({'step': 'post'}
               if 'step' in signature(plt.fill_between).parameters
               else {})
plt.step(recall, precision, color='b', alpha=0.2,
         where='post')
plt.fill_between(recall, precision, alpha=0.2, color='b', **step_kwargs)

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.05])

# tp = 0
# fp = 0
# fn = 0
# tn = 0
#
# for i in range(H):
#     for j in range(W):
#         if output[i][j] == ans[i][j] == 255:
#             tp += 1
#         elif output[i][j] == 255 and ans[i][j] == 0:
#             fp += 1
#         elif output[i][j] == 0 and ans[i][j] == 255:
#             fn += 1
#         elif output[i][j] == ans[i][j] == 0:
#             tn += 1
# print(tp, fp, fn, tn)
# precision = tp / (tp + fp)
# recall = tp / (tp + fn)
# print('precision:' + str(precision))
# print('recall:' + str(recall))
# print('F-measure:' + str(2 * precision * recall / (precision + recall)))
# print('auc', average_precision_score(ans_flat, im3_flat))

plt.show()
