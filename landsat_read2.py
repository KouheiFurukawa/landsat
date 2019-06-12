import numpy as np
import matplotlib.pyplot as plt
import cv2

if __name__ == "__main__":

    xi = 4000
    yi = 1300
    W = 20
    H = 20

    filename = "LC08_L1TP_108036_20190418_20190423_01_T1_B4.TIF"

    try:
        f = open(filename, 'r')
    except:
        print(IOError, 'cannot open ', filename)
        exit()
    f.close()

    im = cv2.imread(filename, -1) # -1 for 16bit image

    print(im.shape)

    im1 = im[yi:yi+H,xi:xi+W] # extract subimage
    im2 = np.array([[8000 - 400 * k for k in range(20)]] * 20)
    print(im2)
    plt.imshow(im2)
    plt.show()
