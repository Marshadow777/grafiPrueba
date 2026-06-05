import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
ret, img = cap.read()
x,y,z = img.shape
fondo = np.zeros((x,y), np.uint8)
#cv.imshow('fondo', fondo)
#img2 = np.zeros((x,y), np.uint8)
#img1a = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

while True:
    ret, img = cap.read()

    if(ret):
        r,g,b = cv.split(img)
        mr = cv.merge([fondo,fondo,r])
        mg = cv.merge([fondo,g,fondo])
        mb = cv.merge([b,fondo,fondo])
        nv = cv.merge([b,r,g])

        """for i in range(x):
            for j in range(y):
                img2[i,j] = 255 - img1a[i,j]"""

        #cv.imshow('Videonv', img2)
        cv.imshow('Videor', mr)
        cv.imshow('Videog', mg)
        cv.imshow('Videob', mb)
        cv.imshow('Video', img)
    else:
        print('Conexion fallida')
        break
    k = cv.waitKey(1)
    if k==27:
        break
cap.release()
cv.destroyAllWindows()