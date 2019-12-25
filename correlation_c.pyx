from __future__ import division
import numpy as np
cimport numpy as np

DTYPE = np.uint8
DTYPEF = np.float

ctypedef np.uint8_t DTYPE_t
ctypedef np.float_t DTYPEF_t


def correlation_c(np.ndarray[DTYPE_t, ndim=2] img1, np.ndarray[DTYPE_t, ndim=2] img2, int win, int size):
    cdef np.ndarray[double, ndim=2] result
    result = np.zeros((size - win + 1, size - win + 1), dtype=np.float)
    cdef np.ndarray[DTYPE_t, ndim=2] win1
    cdef np.ndarray[DTYPE_t, ndim=2] win2
    win1 = np.zeros((win, win), dtype=DTYPE)
    win2 = np.zeros((win, win), dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=1] win1_flat
    cdef np.ndarray[DTYPE_t, ndim=1] win2_flat
    win1_flat = np.zeros(win * win, dtype=DTYPE)
    win2_flat = np.zeros(win * win, dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=2] x
    x = np.zeros((2, win * win), dtype=DTYPE)

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
