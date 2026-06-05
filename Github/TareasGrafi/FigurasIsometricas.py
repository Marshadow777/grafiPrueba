import cv2 as cv
import numpy as np
import math

img = np.ones((1000,1000), dtype=np.uint8)*255

def printCube(x,y,long):
    cv.line(img,(x,y), (x,y+long),(0,0,0), 5)
    cv.line(img,(x,y), (int(x+(long*(math.sqrt(3))/2)),y-int(long/2)),(0,0,0), 5)
    cv.line(img, (int(x+(long*(math.sqrt(3))/2)),y-int(long/2)),(int(x+(long*(math.sqrt(3)))),y),(0,0,0), 5)
    cv.line(img,(x,y), (int(x+(long*(math.sqrt(3))/2)),y+int(long/2)),(0,0,0), 5)
    cv.line(img, (int(x+(long*(math.sqrt(3))/2)),y+int(long/2)),(int(x+(long*(math.sqrt(3)))),y),(0,0,0), 5)
    cv.line(img,(x,y+long), (int(x+(long*(math.sqrt(3))/2)),y+int(long/2)+long),(0,0,0), 5)
    cv.line(img, (int(x+(long*(math.sqrt(3))/2)),y+int(long/2)+long),(int(x+(long*(math.sqrt(3)))),y+long),(0,0,0), 5)
    cv.line(img, (int(x+(long*(math.sqrt(3))/2)),y+int(long/2)), (int(x+(long*(math.sqrt(3))/2)),y+int(long/2)+long), (0,0,0), 5)
    cv.line(img, (int(x+(long*(math.sqrt(3)))),y), (int(x+(long*(math.sqrt(3)))),y+long),(0,0,0), 5)

printCube(400,800,100)
printCube(488,650,100)
printCube(574,800,100)
printCube(226,800,100)
printCube(313,650,100)
printCube(400,500,100)



cv.imshow("Imagen",img)
cv.waitKey(0)
cv.destroyAllWindows()


