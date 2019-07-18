import numpy as np
import matplotlib.pyplot as plt
import cv2
from pylab import *
from sklearn.decomposition import PCA
import itertools

filepath = ""  # please change here
if __name__ == "__main__":
    #######################################################################################
    # Read Landsat-8 data
    #######################################################################################
    # coordinates for subimage
    xi = 4000
    yi = 3000
    W = 1000
    H = 1000
    # number of bins for histogram
    num_bins = 50

    # array for multispectral subimages
    landsat_subimg = np.zeros((9,W,H))

    # Read data and extract subimages
    for b in range(9):
        if b <= 6:
            band = b+1
            filename = "LC08_L1TP_111036_20180607_20180615_01_T1_B"+str(band)+".TIF"
        else:
            band = b+3
            filename = "LC08_L1TP_111036_20180607_20180615_01_T1_B"+str(band)+".TIF"
        img = cv2.imread(filepath+filename,-1)
#        img = cv2.LoadImageM(filepath+filename,cv2.CV_LOAD_IMAGE_UNCHANGED)
        subimg = img[yi:yi+H, xi:xi+W]  # extract subimage

        landsat_subimg[b, :, :] = np.array(subimg)

        figure(1)
        # plt.set_cmap('gray')
        plt.subplot(3,3,b+1)
        plt.imshow(landsat_subimg[b, :, :])
        plt.title('Band'+str(band))

        figure(2)
        plt.subplot(3, 3, b+1)
        x = landsat_subimg[b, :, :].reshape((W*H,1))
        n, bins, patches = plt.hist(x, num_bins,  facecolor='red', alpha=0.5)
        # plt.xlim(0,255)
        plt.xlabel('DN')
        plt.ylabel('Num. of Pixels')
        plt.title('Band'+str(band))

    # RGB image
    enhance = np.array([[6000, 15000], [7000, 12000], [8000, 12000]])
    rgb = np.zeros((3, W, H))
    for i in range(3):
        tmp = (landsat_subimg[3-i, :, :]-enhance[i, 0])*255/(enhance[i, 1]-enhance[i, 0])
        # tmp[np.nonzero(tmp<0)] = 0
        tmp[np.nonzero(tmp>255)] = 255
        tmp[np.nonzero(tmp<0  )] =   0
        print(np.amax(tmp), ' ', np.amin(tmp))
        rgb[i,:,:] = tmp

    figure(3)
    plt.imshow(np.uint8(rgb.transpose([1,2,0])))
    plt.title('RGB image')
    # save RGB image
    save_array_ori = rgb.transpose([1,2,0])
    save_array = save_array_ori.copy()
    save_array[:,:,0] = save_array_ori[:,:,2].copy()
    save_array[:,:,2] = save_array_ori[:,:,0].copy()
#    save_img = array2cv(np.uint8(save_array))
#    cv.SaveImage('Sample1.png',save_img)
    cv2.imwrite("sample.png", save_array)

    # NDVI image
    NDVI = (landsat_subimg[4,:,:]-landsat_subimg[3,:,:])/(landsat_subimg[4,:,:]+landsat_subimg[3,:,:])
    figure(4)
    plt.imshow(NDVI)
    plt.title('NDVI image')

    # PCA
    X = np.stack([landsat_subimg[8,:,:].reshape(-1,), landsat_subimg[7,:,:].reshape(-1,)], 1)

    pca = PCA(n_components=2)
    pca.fit(X)
    Xd = pca.transform(X)
    figure(5)
    plt.imshow(Xd[:, 0].reshape(W, H))
    figure(6)
    plt.scatter(X[:, 0], X[:, 1], s=1)
    plt.axis('equal')
    figure(7)
    plt.scatter(Xd[:, 0], Xd[:, 1], s=1)
    plt.axis('equal')

    plt.show()
