# coding:utf-8
import matplotlib.pyplot as plt
import cv2
from sklearn.metrics import auc
from inspect import signature
from module_change_detection import *

W = 4000
H = 4000
xi = 8000 - W // 2
yi = 14500 - H // 2
win = 3

filename = "PRD_RGB_20180708_004_0000208911.tif"
im = cv2.imread(filename)

# 読み込み
im1 = im[yi:yi + W, xi:xi + H, 2]  # extract subimage
plt.figure(1)
plt.imshow(im1, cmap='gray')
plt.colorbar()

im2 = im[yi:yi + W, xi:xi + H, 0]  # extract subimage
plt.figure(2)
plt.imshow(im2, cmap='gray')
plt.colorbar()

# 中央値フィルタ
im1_median = cv2.medianBlur(im1, 5)
im1_median = cv2.medianBlur(im1_median, 5)
im2_median = cv2.medianBlur(im2, 5)
im2_median = cv2.medianBlur(im2_median, 5)

# Lee-sigmaフィルタ
im1_lee = lee_sigma(im1, win, 1)
im1_lee = lee_sigma(im1_lee, win, 1)
im2_lee = lee_sigma(im2, win, 1)
im2_lee = lee_sigma(im2_lee, win, 1)

result = mixed_information(0.17, im1, im2, W)
output = thresholding_new(result, im1, im2, W)
output2 = cv2.merge((output, im1, im1))
plt.figure(5)
plt.imshow(output2)

# ground_truth
g = cv2.imread('ground_truth_mabi.tif')
ans = g[2000 - W // 2:2000 + W // 2, 2000 - W // 2:2000 + W // 2, 0]
plt.figure(6)
ans = ground_truth(ans, W)
plt.imshow(ans)

# 計算
a_list = [0.05 * i for i in range(-20, 21)]
recall_mi = [[0.0], [0.0], [0.0], [0.0]]
precision_mi = [[1.0], [1.0], [1.0], [1.0]]
p1 = [get_p_map(im1, W), get_p_map(im1_median, W), get_p_map(im1_lee, W), get_p_map(im1, W)]
p2 = [get_p_map(im2, W), get_p_map(im2_median, W), get_p_map(im2_lee, W), get_p_map(im2, W)]
p12 = [get_p_map_2d(im1, im2, W), get_p_map_2d(im1_median, im2_median, W), get_p_map_2d(im1_lee, im2_lee, W),
       get_p_map_2d(im1, im2, W)]

for i in range(4):
    for alpha in a_list:
        if i <= 2:
            pr = clustering(p1[i], p2[i], p12[i], alpha, W, ans)
            recall_mi[i].append(pr[1])
            precision_mi[i].append(pr[0])
        else:
            pr = clustering_new(im1, im2, p1[i], p2[i], p12[i], alpha, W, ans)
            recall_mi[i].append(pr[1])
            precision_mi[i].append(pr[0])
    print('recall', recall_mi[i])
    print('precision', precision_mi[i])

print('フィルターなしのAUC', auc(recall_mi[0], precision_mi[0]))
print('中央値フィルターのAUC', auc(recall_mi[1], precision_mi[1]))
print('Lee-sigmaフィルターのAUC', auc(recall_mi[2], precision_mi[2]))
print('提案手法のAUC', auc(recall_mi[3], precision_mi[3]))

plt.figure(7)
step_kwargs = ({'step': 'post'}
               if 'step' in signature(plt.fill_between).parameters
               else {})
plt.step(recall_mi[0], precision_mi[0], color='b', alpha=0.2,
         where='post', label='no filter')
plt.step(recall_mi[1], precision_mi[1], color='r', alpha=0.2,
         where='post', label='median filter')
plt.step(recall_mi[2], precision_mi[2], color='g', alpha=0.2,
         where='post', label='Lee-sigma filter')
plt.step(recall_mi[3], precision_mi[3], color='orange', alpha=0.2,
         where='post', label='suggested method')
plt.title("PR curve of filters")
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.05])
plt.legend()

plt.figure(8)
step_kwargs = ({'step': 'post'}
               if 'step' in signature(plt.fill_between).parameters
               else {})
plt.step(recall_mi[0], precision_mi[0], color='b', alpha=0.2,
         where='post', label='no filter')
plt.step(recall_mi[1], precision_mi[1], color='r', alpha=0.2,
         where='post', label='median filter')
plt.step(recall_mi[2], precision_mi[2], color='g', alpha=0.2,
         where='post', label='Lee-sigma filter')
plt.step(recall_mi[3], precision_mi[3], color='orange', alpha=0.2,
         where='post', label='suggested method')
plt.fill_between(recall_mi[0], precision_mi[0], alpha=0.2, color='b', **step_kwargs)
plt.fill_between(recall_mi[1], precision_mi[1], alpha=0.2, color='r', **step_kwargs)
plt.fill_between(recall_mi[2], precision_mi[2], alpha=0.2, color='g', **step_kwargs)
plt.fill_between(recall_mi[3], precision_mi[3], alpha=0.2, color='orange', **step_kwargs)

plt.title("PR curve of filters")
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.05])
plt.legend()

plt.show()
