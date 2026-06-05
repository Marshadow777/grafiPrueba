import cv2 as cv
import numpy as np

img = np.ones([800,800], np.uint8)*255

verde = 165
cafe = 100
naranja = 150

def printPixel(x,y,c):
    for i in range(50):
        for j in range(50):
            img[(x*50)+i][(y*50)+j] = c
            

for i in range(16):
    for j in range(16):
        if i==0 and j>=6 and j<12:
            printPixel(i,j,verde)
        elif i==1 and j>=5 and j<13:
            printPixel(i,j,verde)
        elif i==2 and j>=5 and j<6:
            printPixel(i,j,verde)
        elif i==2 and j>=6 and j<12:
            printPixel(i,j,cafe)
        elif i==2 and j>=11 and j<13:
            printPixel(i,j,verde)
        elif i==3 and j>=5 and j<13:
            printPixel(i,j,cafe)
        elif i>=2 and i<6 and (j==3 or j==14):
            printPixel(i,j,naranja)
        elif i>=4 and i<7 and (j==4 or j==13):
            printPixel(i,j,naranja)
        elif i>=4 and i<6 and (j==5 or j==12):
            printPixel(i,j,cafe)
        elif i==4  and (j==7 or j==10):
            printPixel(i,j,verde)
        elif i==5  and (j==7 or j==10):
            printPixel(i,j,cafe)
        elif i>=4 and i<6 and (j==6 or j==11 or j==8 or j==9):
            printPixel(i,j,naranja)
        elif i==6 and j>=5 and j<=12:
            printPixel(i,j,naranja)
        elif i==7 and ((j>=4 and j<=5)or(j>=12 and j<=13)):
            printPixel(i,j,verde)
        elif i==7 and ((j>=6 and j<=7)or(j>=10 and j<=11)):
            printPixel(i,j,naranja)
        elif i==7 and (j==8 or j==9 or j == 14):
            printPixel(i,j,cafe)
        elif i==6 and j == 14:
            printPixel(i,j,cafe)
        elif i==8:
            if (j>=2 and j<=6) or (j>=13 and j<=15):
                printPixel(i,j,cafe)
            elif j>=7 and j<=10:
                printPixel(i,j,naranja)
            elif j==11 or j==12:
                printPixel(i,j,verde)
        elif i == 9:
            if(j>=1 and j<=2) or (j>=4 and j<=7) or (j>=14 and j<=15):
                printPixel(i,j,cafe)
            elif j==3 or j==13:
                printPixel(i,j,naranja)
            elif j>=8 and j<=12:
                printPixel(i,j,verde)
        elif i == 10:
            if j==1 or  j==5 or j==6 or j==8 or j==9 or j==15:
                printPixel(i,j,cafe)
            elif (j>=2 and j<=4) or j==7 or(j>=12 and j<=14):
                printPixel(i,j,naranja)
            elif j==11 or j==10:
                printPixel(i,j,verde)
        elif i == 11:
            if j==1 or  j==2 or (j>=4 and j<=6) or (j>=9 and j<=12):
                printPixel(i,j,cafe)
            elif j==3 or j==7 or (j>=13 and j<=15):
                printPixel(i,j,naranja)
            elif j==8:
                printPixel(i,j,verde)
        elif i == 12:
            if j==1 or  j==2 or (j>=4 and j<=6) or (j>=8 and j<=9):
                printPixel(i,j,cafe)
            elif j==3 or j==7 or j==14:
                printPixel(i,j,naranja)
            elif j>=10 and j<=13:
                printPixel(i,j,verde)
        elif i == 13:
            if j>=1 and j<=6:
                printPixel(i,j,cafe)
            elif j==7:
                printPixel(i,j,naranja)
            elif j>=8 and j<=12:
                printPixel(i,j,verde)
        elif i == 14:
            if j==7 or (j>=10 and j<=12):
                printPixel(i,j,cafe)
            elif j>=2 and j<=6:
                printPixel(i,j,naranja)
        elif i==15 and j>=5 and j<=7:
            printPixel(i,j,cafe)
            
#img = cv.imread("C:\\Users\\marce\\Downloads\\images.png")
cv.imshow('img', img)
cv.waitKey()
cv.destroyAllWindows()