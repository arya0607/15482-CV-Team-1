import numpy as np
import cv2
from cv_utils import *
from filterColor import createMask, transformFromBGR


# Detect the plants in the image. Return a mask (black/white mask, where 0
# indicates no plants and 255 indicates plants)
def classifyFoliage(image):
    foliage_mask = np.zeros(image.shape[0:2], np.uint8)
    # Your code goes here:
    # Create a mask that has 255 where there is part of a plant in the image
    #   and 0 everywhere else
    # BEGIN STUDENT CODE
    #H - 22, 53
    #S - 0, 255
    #V - 24, 123
    hsvImage = transformFromBGR(image, 'HSV')
    rVals = [(22, 53), (0, 255), (24, 123)]
    mask = createMask(hsvImage, rVals, 'HSV')
    foliage_mask = mask
    # END STUDENT CODE
    return foliage_mask


# Given the foliage mask (as would be returned from classifyFoliage), 
#   return the height in cms the tallest plant that crosses in front 
#   of the measuring stick. Return None if no foliage overlaps the stick
def measureHeight(foliage_mask):
    height = None
    # Your code goes here:
    # Find the maximum height of plants that overlap the measuring stick
    #   in the foliage_mask
    # BEGIN STUDENT CODE
    # END STUDENT CODE
    return height

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
    # END STUDENT CODE

    A = np.zeros((9, 9), np.float)
    # Your code goes here:
    # Fill in the rows of the matrix, according to the notes
    # BEGIN STUDENT CODE
    # END STUDENT CODE
    d = np.zeros((1,9))
    # Your code goes here:
    # Fill in the d vector with the "goal" colors 
    # BEGIN STUDENT CODE
    # END STUDENT CODE

    x = np.matmul(np.matmul(np.linalg.pinv(np.matmul(A.T, A)), A.T), d.T)
    T = x.reshape((3,3))

    corrected_image = image.copy()
    # Your code goes here:
    # Apply the transform to the pixels of the image and return the new image
    # BEGIN STUDENT CODE
    # END STUDENT CODE

    return corrected_image

def classifyFoliageCorrected(image):
    # You can use these as "ground truth" or substitute your own
    blue_goal =  [150, 75, 75]
    green_goal = [75, 150, 75]
    red_goal =   [75, 75, 150]

    # colorCorrect the image and then use classifyFoliage to
    corrected_image = colorCorrect(image, blue_goal, green_goal, red_goal)
    # detect the plants in the image
    # note that you will probably need to change the filter values to
    #   work well for the color-corrected images
    # BEGIN STUDENT CODE
    # END STUDENT CODE
    foliage_mask = classifyFoliage(corrected_image)
    return foliage_mask
