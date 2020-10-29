import numpy as np
import cv2
import sys

# get statistics on water from image
image = cv2.cvtColor(cv2.imread(sys.argv[1]), cv2.COLOR_BGR2HSV)
image = image[image != 0]
# h = image[0::3]
# s = image[1::3]
# v = image[2::3]
# for i in range(0, len(h)):
#     print(str(h[i]) + ' ' + str(s[i]) + ' ' + str(v[i]))

# split into small sections with patterns
# alpha shape convex hull python
# https://stackoverflow.com/questions/6833243/how-can-i-find-the-alpha-shape-concave-hull-of-a-2d-point-cloud