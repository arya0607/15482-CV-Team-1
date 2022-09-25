import cv2 as cv
import numpy as np
import vision

im = cv.imread('images/day05.jpg')
img = vision.classifyFoliage(im)
# left top, right top, right bottom, left bottom
c = np.array([[1960, 295], [2069, 287], [1942, 2088], [1860, 2085]])
img2 = cv.drawContours(img, [c], 0, 128, -1)  # B, G, R
print(img2.shape)
cv.imwrite('bla.png', img2)
