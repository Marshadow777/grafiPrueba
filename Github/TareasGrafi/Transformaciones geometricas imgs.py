import cv2 as cv
import numpy as np
import math


img = cv.imread("C:\\Users\\marce\\Downloads\\triforce.jpg",0)

x,y = img.shape

# Crear una imagen vacía para la traslación
translated_img = np.zeros((x, y), dtype=np.uint8)

# Obtener el tamaño de la imagen
x, y = img.shape

# Crear una imagen vacía para la traslación
translated_img = np.zeros((x, y), dtype=np.uint8)

# Definir el desplazamiento en x e y
dx, dy = 100, 50

# Trasladar la imagen
for i in range(x):
    for j in range(y):
        new_x = i + 20
        new_y = j + 30
        if 0 <= new_x < x and 0 <= new_y < y:
            translated_img[new_x, new_y] = img[i, j]

# Crear una imagen vacía para almacenar el resultado

rotated_img = np.zeros((x*2, y*2), dtype=np.uint8)

xx, yy = rotated_img.shape
# Calcular el centro de la imagen
cx, cy = int(x  // 2), int(y  // 2)

# Definir el ángulo de rotación (en grados) y convertirlo a radianes
angle = 45
theta = math.radians(angle)

# Rotar la imagen
for i in range(x):
    for j in range(y):
        new_x = int((j - cx) * math.cos(theta) - (i - cy) * math.sin(theta) + cx)
        new_y = int((j - cx) * math.sin(theta) + (i - cy) * math.cos(theta) + cy)
        if 0 <= new_x < 2*x and 0 <= new_y < 2*y:
            rotated_img[new_y, new_x] = img[i, j]

x, y = img.shape
# Definir el factor de escala
scale_x, scale_y = 2, 2
# Crear una nueva imagen para almacenar el escalado
scaled_img = np.zeros((int(x * scale_y), int(y * scale_x)), dtype=np.uint8)
# Aplicar el escalado
for i in range(x):
    for j in range(y):
                   #orig_x = int(i * scale_y)
                   #orig_y = int(j * scale_x)
            scaled_img[i*2, j*2] = img[i, j]

# Mostrar la imagen original y la escalada
cv.imshow('Imagen Escalada (modo raw)', scaled_img)

# Mostrar la imagen original y la rotada
cv.imshow('Imagen Rotada (modo raw)', rotated_img)

# Mostrar la imagen original y la trasladada
cv.imshow('Imagen Original', img)
cv.imshow('Imagen Trasladada', translated_img)
cv.waitKey(0)
cv.destroyAllWindows()