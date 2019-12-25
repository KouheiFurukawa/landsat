import matplotlib.pyplot as plt
import cv2
from pylab import *

filename = 'ground_truth_mabi.tif'
im = cv2.imread(filename)

plt.imshow(im)
plt.show()
