import cv2 as cv
import numpy as np

lienzo = np.ones((500, 500, 3), dtype=np.uint8)*255

t_values = np.arange(0, 2 * np.pi, 0.01) 

x_valores = 250 + 150 * np.sin(3 * t_values)
y_valores = 250 + 150 * np.sin(2 * t_values)


for x, y in zip(x_valores, y_valores):
    x = int(x)
    y = int(y)
    cv.circle(lienzo,(x,y), 5, (0,0,0), -1)

cv.imshow("Dibujo", lienzo)
cv.waitKey(0)
cv.destroyAllWindows()