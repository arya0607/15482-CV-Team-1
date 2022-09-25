import cv2 as cv
import numpy as np

img = cv.imread('day02.jpg')
c = np.array([[1960, 295], [2069, 287], [1942, 2088], [1860, 2085]])
img2 = cv.drawContours(img, [c], 0, 255,-1)
cv.imwrite('bla.png', img2)