import numpy as np
import matplotlib.pyplot as plt
import cv2

if __name__ == "__main__":

    xi = 4300
    yi = 3700
    W = 300
    H = 300

    # filename = "PRD_RGB_20180708_004_0000208911.tif"
    filename = "LC08_L1TP_111036_20180420_20180502_01_T1_B5.tif"

    try:
        f = open(filename, 'r')
    except:
        print(IOError, 'cannot open ', filename)
        exit()
    f.close()

    im = cv2.imread(filename, -1)  # -1 for 16bit image

    print(im.shape)

    im1 = im[yi:yi + H, xi:xi + W]  # extract subimage
    print(im1)
    plt.imshow(im1)
    plt.show()
