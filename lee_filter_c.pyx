from __future__ import division
import numpy as np
cimport numpy as np

DTYPE = np.uint8

ctypedef np.uint8_t DTYPE_t

cdef delta(int x, double m, double s):
    if (1 - 2 * s) * m <= x <= (1 + 2 * s) * m:
        return 1
    else:
        return 0

def lee_sigma(np.ndarray[DTYPE_t, ndim=2] img, int win, int k):
    cdef int m = (win - 1) // 2
    cdef double v, sd, dz
    cdef int pm, d
    cdef np.ndarray[DTYPE_t, ndim=2] sub_img
    for i in range(m, 4000 - m):
        for j in range(m, 4000 - m):
            sub_img = img[i - m:i + m + 1, j - m:j + m + 1]
            pm = sub_img[m][m]
            v = 0
            for p in range(win):
                for q in range(win):
                    v += (pm - sub_img[p][q]) ** 2

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
    return img
