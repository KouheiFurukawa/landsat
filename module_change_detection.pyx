import numpy as np
cimport numpy as np
from libc.math cimport log2

ctypedef np.float_t DTYPE_f
ctypedef np.uint8_t DTYPE_t
ctypedef np.int8_t DTYPE_d

def hist(np.ndarray[DTYPE_t, ndim=2] image, int size):
    cdef np.ndarray[DTYPE_t, ndim=1] image_flat
    image_flat = np.zeros(size * size, dtype=np.uint8)
    image_flat = image.flatten()
    return np.histogram(image_flat, bins=np.linspace(0, 256, 257))[0] / (size * size)

def hist2d(np.ndarray[DTYPE_t, ndim=2] image1, np.ndarray[DTYPE_t, ndim=2] image2, int size):
    cdef np.ndarray[DTYPE_t, ndim=1] image1_flat
    cdef np.ndarray[DTYPE_t, ndim=1] image2_flat
    image1_flat = np.zeros(size * size, dtype=np.uint8)
    image1_flat = np.zeros(size * size, dtype=np.uint8)
    image1_flat = image1.flatten()
    image2_flat = image2.flatten()
    return np.histogram2d(image1_flat, image2_flat, [np.linspace(0, 256, 257), np.linspace(0, 256, 257)])[0] / (
            size * size)

def mixed_information(double a, np.ndarray[DTYPE_t, ndim=2] im1, np.ndarray[DTYPE_t, ndim=2] im2,
                      int size):
    cdef np.ndarray[double, ndim=2] result
    cdef np.ndarray[double, ndim=1] px
    cdef np.ndarray[double, ndim=1] py
    cdef np.ndarray[double, ndim=2] pxy

    result = np.zeros((size, size), dtype=np.float)
    px = np.zeros(257, dtype=np.float)
    py = np.zeros(257, dtype=np.float)
    pxy = np.zeros((size, size), dtype=np.float)

    px = hist(im1, size)
    py = hist(im2, size)
    pxy = hist2d(im1, im2, size)

    cdef int k
    cdef int l
    for k in range(size):
        for l in range(size):
            p1 = px[im1[k][l]]
            p2 = py[im2[k][l]]
            p12 = pxy[im1[k][l]][im2[k][l]]
            result[k][l] = (1 + a) * log2(p12) - log2(p1 * p2)

    return result

def thresholding(np.ndarray[double, ndim=2] cmap, int size):
    cdef np.ndarray[DTYPE_t, ndim=2] out
    out = np.zeros((size, size), dtype=np.uint8)
    cdef int k
    cdef int l
    for k in range(size):
        for l in range(size):
            if cmap[k][l] < 0:
                out[k][l] = 255
    return out

def thresholding_new(np.ndarray[double, ndim=2] cmap, np.ndarray[DTYPE_t, ndim=2] image1,
                     np.ndarray[DTYPE_t, ndim=2] image2, int size):
    cdef np.ndarray[DTYPE_t, ndim=2] out
    out = np.zeros((size, size), dtype=np.uint8)
    cdef int k
    cdef int l
    for k in range(size):
        for l in range(size):
            if cmap[k][l] < 0 and <int> image1[k][l] - <int> image2[k][l] > 3:
                out[k][l] = 255
    return out

def get_p_map(np.ndarray[DTYPE_t, ndim=2] image, int size):
    cdef np.ndarray[double, ndim=1] p
    p = hist(image, size)
    cdef np.ndarray[double, ndim=2] out
    out = np.zeros((size, size), dtype=np.float)
    for k in range(size):
        for l in range(size):
            out[k][l] = p[image[k][l]]
    return out

def get_p_map_2d(np.ndarray[DTYPE_t, ndim=2] image1, np.ndarray[DTYPE_t, ndim=2] image2, int size):
    cdef np.ndarray[double, ndim=2] p
    p = hist2d(image1, image2, size)
    cdef np.ndarray[double, ndim=2] out
    out = np.zeros((size, size), dtype=np.float)
    for k in range(size):
        for l in range(size):
            out[k][l] = p[image1[k][l]][image2[k][l]]
    return out

def clustering_new(np.ndarray[DTYPE_t, ndim=2] image1, np.ndarray[DTYPE_t, ndim=2] image2,
                   np.ndarray[double, ndim=2] p1,
                   np.ndarray[double, ndim=2] p2, np.ndarray[double, ndim=2] p12, double a,
                   int size, np.ndarray[DTYPE_t, ndim=2] ans):
    cdef np.ndarray[double, ndim=2] result
    result = np.zeros((size, size), dtype=np.float)

    cdef int tp, fp, fn, tn
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    cdef int k
    cdef int l

    for k in range(size):
        for l in range(size):
            result[k][l] = (1 + a) * log2(p12[k][l]) - log2(p1[k][l] * p2[k][l])

    for k in range(size):
        for l in range(size):
            if result[k][l] < 0 and <int> image1[k][l] - <int> image2[k][l] > 0:
                if ans[k][l] == 1:
                    tp += 1
                else:
                    fp += 1
            else:
                if ans[k][l] == 1:
                    fn += 1
                else:
                    tn += 1
    if tp + fp == 0:
        return [1.0, 0.0]
    else:
        return [<double> tp / (tp + fp), <double> tp / (tp + fn), tp, fp, fn]

def clustering(np.ndarray[double, ndim=2] p1, np.ndarray[double, ndim=2] p2, np.ndarray[double, ndim=2] p12,
               double a,
               int size, np.ndarray[DTYPE_t, ndim=2] ans):
    cdef np.ndarray[double, ndim=2] result
    result = np.zeros((size, size), dtype=np.float)

    cdef int tp, fp, fn, tn
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    cdef int k
    cdef int l

    for k in range(size):
        for l in range(size):
            result[k][l] = (1 + a) * log2(p12[k][l]) - log2(p1[k][l] * p2[k][l])

    for k in range(size):
        for l in range(size):
            if result[k][l] < 0 and ans[k][l] == 1:
                tp += 1
            elif result[k][l] < 0 and ans[k][l] == 0:
                fp += 1
            elif result[k][l] >= 0 and ans[k][l] == 1:
                fn += 1
            elif result[k][l] >= 0 and ans[k][l] == 0:
                tn += 1
    if tp + fp == 0:
        return [1.0, 0.0]
    else:
        return [<double> tp / (tp + fp), <double> tp / (tp + fn), tp, fp, fn]

def correlation_c(np.ndarray[DTYPE_t, ndim=2] img1, np.ndarray[DTYPE_t, ndim=2] img2, int win, int size):
    cdef np.ndarray[double, ndim=2] result
    result = np.zeros((size - win + 1, size - win + 1), dtype=np.float)
    cdef np.ndarray[DTYPE_t, ndim=2] win1
    cdef np.ndarray[DTYPE_t, ndim=2] win2
    win1 = np.zeros((win, win), dtype=np.uint8)
    win2 = np.zeros((win, win), dtype=np.uint8)
    cdef np.ndarray[DTYPE_t, ndim=1] win1_flat
    cdef np.ndarray[DTYPE_t, ndim=1] win2_flat
    win1_flat = np.zeros(win * win, dtype=np.uint8)
    win2_flat = np.zeros(win * win, dtype=np.uint8)
    cdef np.ndarray[DTYPE_t, ndim=2] x
    x = np.zeros((2, win * win), dtype=np.uint8)

    cdef int k
    cdef int l
    for k in range(size - win + 1):
        for l in range(size - win + 1):
            win1 = img1[k:k + win, l:l + win]
            win2 = img2[k:k + win, l:l + win]
            win1_flat = win1.flatten()
            win2_flat = win2.flatten()
            x = np.array([win1_flat, win2_flat])
            cc = np.corrcoef(x)
            if np.isnan(cc[0][1]):
                result[k, l] = 0
            else:
                result[k, l] = -cc[0][1]

    return result

def ground_truth(np.ndarray[DTYPE_t, ndim=2] img, int size):
    cdef np.ndarray[DTYPE_t, ndim=2] out
    out = np.zeros((size, size), dtype=np.uint8)
    cdef int k, l

    for k in range(size):
        for l in range(size):
            if img[k][l] == 255:
                out[k][l] = 1
    return out

def diff(np.ndarray[DTYPE_t, ndim=2] img1, np.ndarray[DTYPE_t, ndim=2] img2, int size):
    cdef np.ndarray[DTYPE_d, ndim=2] out
    cdef int k, l
    out = np.zeros((size, size), dtype=np.int8)

    for k in range(size):
        for l in range(size):
            out[k][l] = img1[k][l] - img2[k][l]
    return out

cdef delta(int x, double m, double s):
    if (1 - 2 * s) * m <= x <= (1 + 2 * s) * m:
        return 1
    else:
        return 0

def lee_sigma(np.ndarray[DTYPE_t, ndim=2] img, int win, int k):
    cdef int m = 1
    cdef double v, sd, dz
    sd = 0
    v = 0
    cdef int pm, d
    pm = 0
    cdef np.ndarray[DTYPE_t, ndim=2] sub_img
    cdef np.ndarray[DTYPE_t, ndim=1] sub_img_flat
    cdef np.ndarray[DTYPE_t, ndim=2] out
    sub_img = np.zeros((win, win), dtype=np.uint8)
    sub_img_flat = np.zeros(win * win, dtype=np.uint8)
    out = np.zeros((4000, 4000), dtype=np.uint8)
    cdef int i, j, p, q
    for i in range(m, 4000 - m):
        for j in range(m, 4000 - m):
            sub_img = img[i - m:i + m + 1, j - m:j + m + 1]
            sub_img_flat = sub_img.flatten()
            sd = np.std(sub_img_flat)
            dz = 0
            d = 0

            for p in range(win):
                for q in range(win):
                    dz += delta(sub_img[p][q], pm, sd) * sub_img[p][q]
                    d += delta(sub_img[p][q], pm, sd)

            if d <= k:
                out[i][j] = np.round(
                    (<int> img[i - 1][j + 1] + <int> img[i + 1][j + 1] + <int> img[i - 1][j - 1] + <int> img[i + 1][
                        j - 1]) * 0.25)
            else:
                out[i][j] = dz // d
    return out
