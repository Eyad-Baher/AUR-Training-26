import cv2
import numpy as np


image = cv2.imread(r"Phase3\workshop1\task2.jpg")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_orange = np.array([5,100,100])
upper_orange = np.array([25,255,255])

l_red = np.array([0,100,100])
h_red = np.array([10,255,255])

l_green = np.array([35,80,80])
h_green = np.array([90,255,255])

orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)
red_mask = cv2.inRange(hsv,l_red,h_red)
green_mask = cv2.inRange(hsv,l_green,h_green)

image[red_mask>0] = (0,255,0)
image[orange_mask>0] = (0,0,255)
image[green_mask>0] = (0,165,255)

cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()
