import cv2 as cv
import numpy as np


def printC(i,j):
    img = np.ones((500, 500, 3), dtype="uint8")*255
    cv.circle(img, (i,j),20,(255,0,0), -1)
    cv.imshow('img', img)
    
    cv.waitKey(10)

img = np.ones((500, 500, 3), dtype="uint8")*255

reverseI = False
reverseJ = False
i=j=10

while True:
    if reverseI:
        i = i-4
    else:
        i = i+2
    if reverseJ:
        j = j-3
    else:
        j = j+5
    if i>=490 or i<=10:
        reverseI = not reverseI
    if j>=490 or j<=10:
        reverseJ = not reverseJ
    
    printC(i,j)

    
    


cv.waitKey(0)
cv.destroyAllWindows