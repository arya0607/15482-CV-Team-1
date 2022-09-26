import copy
import numpy as np
import cv2
from cv_utils import *
from filterColor import createMask, transformFromBGR

cv = cv2
# Detect the plants in the image. Return a mask (black/white mask, where 0
# indicates no plants and 255 indicates plants)


def classifyFoliage(image, rVals=None):
    foliage_mask = np.zeros(image.shape[0:2], np.uint8)
    # Your code goes here:
    # Create a mask that has 255 where there is part of a plant in the image
    #   and 0 everywhere else
    # BEGIN STUDENT CODE
    hsvImage = transformFromBGR(image, 'HSV')
    if rVals is None:
        rVals = [(22, 70), (92, 255), (24, 150)]
    foliage_mask = createMask(hsvImage, rVals, 'HSV')
    print(foliage_mask.shape)
    print(foliage_mask)
    return foliage_mask  # 2464 * 3280, y * x
    # END STUDENT CODE

# Given the foliage mask (as would be returned from classifyFoliage),
#   return the height in cms the tallest plant that crosses in front
#   of the measuring stick. Return None if no foliage overlaps the stick


def measureHeight(foliage_mask):
    height = None
    # Your code goes here:
    # Find the maximum height of plants that overlap the measuring stick
    #   in the foliage_mask
    # BEGIN STUDENT CODE
    c = np.array([[1970, 295], [2000, 287], [1920, 2088], [1890, 2085]])
    color = 128
    (m, n) = foliage_mask.shape
    fm = copy.deepcopy(foliage_mask)
    blue_stick = cv.drawContours(
        foliage_mask, [c], 0, color, -1)  # B, G, R
    heightMap = {9: 350,
                 8: 585,
                 7: 813,
                 6: 1010,
                 5: 1206,
                 4: 1375,
                 3: 1550,
                 2: 1714,
                 1: 1860,
                 0: 2001,
                 }
    for i in range(m):
        for j in range(n):
            hm = heightMap
            if blue_stick[i, j] == color and fm[i, j] == 255:
                for h in range(9, 0, -1):
                    if i <= hm[h - 1]:
                        return (h - 1) + ((i - hm[h - 1]) / (hm[h] - hm[h - 1]))
    # END STUDENT CODE
    return None

# Use the color calibration squares to find a transformation that will
#   color-correct the image such that the mean values of the calibration
#   squares are the given "goal" colors.
# Return the color-corrected image


def colorCorrect(image, blue_goal, green_goal, red_goal):
    # Your code goes here:
    # Find a transform c' = T c, c is the pixel value in the image,
    #   c' is the transformed pixel, and T is the 3x3 transformation matrix
    # Do this by solving d = A x, as per the lecture notes.
    # Note that while the lecture notes describe an affine (3x4) transform,
    #  here we have only 3 colors, so it has to be a Euclidean (3x3) tranform
    # BEGIN STUDENT CODE

    # crop the image to find the mean, image[startY:endY, startX:endX]
    red_square = image[225:400, 1135:1295]  # 99.5
    green_square = image[228:395, 1345:1505]
    blue_square = image[230:405, 1560:1720]

    blue_means = np.mean(blue_square, axis=(0, 1))
    green_means = np.mean(green_square, axis=(0, 1))
    red_means = np.mean(red_square, axis=(0, 1))
    # END STUDENT CODE

    A = np.zeros((9, 9), np.float)
    # Your code goes here:
    # Fill in the rows of the matrix, according to the notes
    # BEGIN STUDENT CODE
    for r in range(3):
        A[r, r*3], A[r, r*3+1], A[r, r*3+2] = blue_means
        A[3+r, r*3], A[3+r, r*3+1], A[3+r, r*3+2] = green_means
        A[6+r, r*3], A[6+r, r*3+1], A[6+r, r*3+2] = red_means
    # END STUDENT CODE
    d = np.zeros((1, 9))
    # Your code goes here:
    # Fill in the d vector with the "goal" colors
    # BEGIN STUDENT CODE
    for c in range(3):
        d[0, c] = blue_goal[c]
        d[0, 3+c] = green_goal[c]
        d[0, 6+c] = red_goal[c]
    # END STUDENT CODE

    x = np.matmul(np.matmul(np.linalg.pinv(np.matmul(A.T, A)), A.T), d.T)
    T = x.reshape((3, 3))

    corrected_image = image.copy()
    # Your code goes here:
    # Apply the transform to the pixels of the image and return the new image
    # BEGIN STUDENT CODE
    a, b, _ = np.shape(image)
    for i in range(a):
        for j in range(b):
            corrected_image[i, j] = np.matmul(T, image[i, j])
    # END STUDENT CODE

    return corrected_image


def classifyFoliageCorrected(image):
    # You can use these as "ground truth" or substitute your own
    blue_goal = [150, 75, 75]
    green_goal = [75, 150, 75]
    red_goal = [75, 75, 150]

    # colorCorrect the image and then use classifyFoliage to
    corrected_image = colorCorrect(image, blue_goal, green_goal, red_goal)
    # detect the plants in the image
    # note that you will probably need to change the filter values to
    #   work well for the color-corrected images
    # BEGIN STUDENT CODE
    rVals = [(), (), ()]  # ToDO
    # END STUDENT CODE
    foliage_mask = classifyFoliage(corrected_image, rVals)
    return foliage_mask
