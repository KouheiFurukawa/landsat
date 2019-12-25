import matplotlib.pyplot as plt
import cv2
from sklearn.metrics import precision_recall_curve
from inspect import signature
from module_change_detection import *

W = 4000
H = 4000
# xi = 13500 - W // 2
# yi = 16500 - H // 2
# W = 512
# H = 512
xi = 8000 - W // 2
yi = 14500 - H // 2
# xi = 15500 - W // 2
# yi = 16200 - H // 256
bins = 256

win = 32

filename = "PRD_RGB_20180708_004_0000208911.tif"

im = cv2.imread(filename, -1)  # -1 for 16bit image

im1 = np.array(im[yi:yi + W, xi:xi + H, 2], dtype=np.uint8)  # extract subimage
plt.figure(1)
plt.imshow(im1, cmap='gray')
plt.colorbar()

im2 = np.array(im[yi:yi + W, xi:xi + H, 0], dtype=np.uint8)  # extract subimage
plt.figure(2)
plt.imshow(im2, cmap='gray')
plt.colorbar()

result = diff(im1, im2, W)
plt.figure(5)
plt.imshow(result)
plt.colorbar()

im3_flat = result.flatten()
m = np.mean(im3_flat)
sd = np.std(im3_flat)

plt.figure(6)
plt.hist(-im3_flat, bins=61, range=(-30, 30))

g = cv2.imread('ground_truth_mabi.tif')
ans = g[:, :, 0]
plt.figure(8)
ans = ground_truth(ans, W)
plt.imshow(ans)
ans_flat = ans.flatten()

plt.figure(7)
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

# 提案手法によるthresholding

d = plt.hist(im3_flat, bins=61, range=(-30, 30))[0]
print(d)

noise = np.zeros(61, dtype=np.float)
for i in range(30, 61):
    if d[i] > 0:
        noise[i] = d[i]
        noise[60 - i] = d[i]

output = np.zeros((W, H), dtype=np.uint8)
for i in range(H):
    for j in range(W):
        if result[i][j] > m + 2 * sd:
            output[i][j] = 255

output = cv2.merge((output, im1, im2))


# cv2.imwrite('diff_map.tif', im3)
# cv2.imwrite('diff_map_th.png', result)

# print(noise)
plt.figure(9)
plt.bar(range(-30, 31), noise, width=1, linewidth=0)

plt.figure(10)
plt.imshow(output)

plt.show()
