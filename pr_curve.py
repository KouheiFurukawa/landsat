import matplotlib.pyplot as plt
import cv2
from sklearn.metrics import precision_recall_curve, auc
from inspect import signature
from module_change_detection import *

W = 4000
H = 4000
xi = 8000 - W // 2
yi = 14500 - H // 2
win = 5

filename = "PRD_RGB_20180708_004_0000208911.tif"
im = cv2.imread(filename)

# 読み込み
im1 = np.array(im[yi:yi + W, xi:xi + H, 2], dtype=np.uint8)  # extract subimage
plt.figure(1)
plt.imshow(im1, cmap='gray')
plt.colorbar()

im2 = np.array(im[yi:yi + W, xi:xi + H, 0], dtype=np.uint8)  # extract subimage
plt.figure(2)
plt.imshow(im2, cmap='gray')
plt.colorbar()

result_diff = diff(im1, im2, W)
plt.figure(3)
plt.imshow(result_diff)
plt.colorbar()
result_diff_flat = result_diff.flatten()

result_corr = correlation_c(im1, im2, win, W + win - 1)
plt.figure(4)
plt.imshow(result_corr)
plt.colorbar()
result_corr_flat = result_corr.flatten()

result_mi = mixed_information(0.17, im1, im2, W)
plt.figure(5)
plt.imshow(result_mi)
plt.colorbar()
result_mi_flat = result_mi.flatten()

# ground_truth
g = cv2.imread('ground_truth_mabi.tif')
ans = g[2000 - W // 2:2000 + W // 2, 2000 - W // 2:2000 + W // 2, 0]
plt.figure(6)
ans = ground_truth(ans, W)
plt.imshow(ans)
ans_flat = ans.flatten()

# pr計算
precision_diff, recall_diff, thresholds_diff = precision_recall_curve(ans_flat, result_diff_flat)
precision_corr, recall_corr, thresholds_corr = precision_recall_curve(ans_flat, result_corr_flat)
print('差分のAUC', auc(recall_diff, precision_diff))
print('相関係数のAUC', auc(recall_corr, precision_corr))

# miの諸量を計算
p1 = get_p_map(im1, W)
p2 = get_p_map(im2, W)
p12 = get_p_map_2d(im1, im2, W)
a_list = [0.05 * i for i in range(-20, 21)]
recall_mi = [0.0]
precision_mi = [1.0]
for alpha in a_list:
    pr = clustering(p1, p2, p12, alpha, W, ans)
    recall_mi.append(pr[1])
    precision_mi.append(pr[0])
print(recall_mi)
print(precision_mi)
print('MIのAUC', auc(recall_mi, precision_mi))

plt.figure(7)
step_kwargs = ({'step': 'post'}
               if 'step' in signature(plt.fill_between).parameters
               else {})
plt.step(recall_diff, precision_diff, color='b', alpha=0.2,
         where='post', label='difference')
plt.step(recall_corr, precision_corr, color='r', alpha=0.2,
         where='post', label='correlation')
plt.step(recall_mi, precision_mi, color='g', alpha=0.2,
         where='post', label='Mixed Information')
plt.title("PR curve of similarity measures")
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.05])
plt.legend()

plt.figure(8)
step_kwargs = ({'step': 'post'}
               if 'step' in signature(plt.fill_between).parameters
               else {})
plt.step(recall_diff, precision_diff, color='b', alpha=0.2,
         where='post', label='difference')
plt.step(recall_corr, precision_corr, color='r', alpha=0.2,
         where='post', label='correlation')
plt.step(recall_mi, precision_mi, color='g', alpha=0.2,
         where='post', label='Mixed Information')

plt.fill_between(recall_diff, precision_diff, alpha=0.2, color='b', **step_kwargs)
plt.fill_between(recall_corr, precision_corr, alpha=0.2, color='r', **step_kwargs)
plt.fill_between(recall_mi, precision_mi, alpha=0.2, color='g', **step_kwargs)

plt.title("PR curve of similarity measures")
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.05])
plt.legend()

plt.show()
