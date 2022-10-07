import cv2 as cv
import numpy as np
import vision

im = cv.imread('images/day05.jpg')
blue_goal = [150, 75, 75]
green_goal = [75, 150, 75]
red_goal = [75, 75, 150]
img = vision.colorCorrect(im, blue_goal, green_goal, red_goal)
cv.imwrite('bla2.png', img)