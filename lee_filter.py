import numpy as np
import matplotlib.pyplot as plt
import cv2
from pylab import *


def delta(x, m, s):
    if (1 - 2 * s) * m <= x <= (1 + 2 * s) * m:
        return 1
    else:
        return 0


def lee_sigma(img, win, k):
    global W, H
    m = (win - 1) // 2
    for i in range(m, 1000 - m):
        for j in range(m, 1000 - m):
            sub_img = img[i - m:i + m + 1, j - m:j + m + 1]
            pm = sub_img[m][m]
            v = 0
            for p in range(win):
                for q in range(win):
                    v += (int(pm) - int(sub_img[p][q])) ** 2

            v /= win ** 2
            sd = v ** 0.5
            dz = 0
            d = 0

            for p in range(win):
                for q in range(win):
                    dz += delta(sub_img[p][q], pm, sd) * sub_img[p][q]
                    d += delta(sub_img[p][q], pm, sd)

            if d <= k:
                img[i][j] = int((img[i - 1][j + 1] + img[i + 1][j + 1] + img[i - 1][j - 1] + img[i + 1][j - 1]) * 0.25)
            else:
                img[i][j] = dz // d


if __name__ == "__main__":
    # ノイズ検証用
    W = 2048
    H = 2048
    xi = 15500 - W // 2
    yi = 16200 - H // 2

    filename = "PRD_RGB_20180708_004_0000208911.tif"
    im = cv2.imread(filename)

    im1 = im[yi:yi + W, xi:xi + H, 2]  # extract subimage
    figure(1)
    plt.imshow(im1, cmap="gray")

    im2 = im[yi:yi + W, xi:xi + H, 0]  # extract subimage
    figure(2)
    plt.imshow(im2, cmap="gray")
    lee_sigma(im2, 5, 2)
    lee_sigma(im2, 5, 2)

    figure(3)
    plt.imshow(im1, cmap="gray")
    figure(4)
    plt.imshow(im2, cmap="gray")

    plt.show()