import cv2 as cv
import numpy as np
import math

def trasladar (img):
    x,y = img.shape

    # Definir el desplazamiento en x e y
    dx = int(input("Cuantos pixeles trasladar en x: "))
    dy = int(input("Cuantos pixeles trasladar en y: "))
    
    # Crear una imagen vacía para la traslación
    translated_img = np.zeros((x+dx, y+dy), dtype=np.uint8)

    # Trasladar la imagen
    for i in range(x):
        for j in range(y):
            new_x = i + dx
            new_y = j + dy
            if 0 <= new_x and 0 <= new_y:
                translated_img[new_x, new_y] = img[i, j]
    return translated_img

def rotar(img):
    x,y = img.shape
    diag = 10 + round(math.sqrt((x*x)+(y*y)))
    rotated_img = np.zeros((diag, diag), dtype=np.uint8)

    xx, yy = rotated_img.shape
    # Calcular el centro de la imagen
    cx, cy = int(x  // 2), int(y  // 2)
    center_rotated = diag // 2

    # Definir el ángulo de rotación (en grados) y convertirlo a radianes
    angle = int(input("Cuantos grados rotar: "))
    theta = math.radians(angle)

    # Rotar la imagen
    for i in range(x):
        for j in range(y):
            new_x = int((j - cx) * math.cos(theta) - (i - cy) * math.sin(theta) + cx)
            new_y = int((j - cx) * math.sin(theta) + (i - cy) * math.cos(theta) + center_rotated)  #round((diag//2))
            if 0 <= new_x < diag and 0 <= new_y < diag:
                rotated_img[new_y, new_x] = img[i, j]
    return rotated_img

def escalar(img):
    x, y = img.shape
    # Definir el factor de escala
    scale_x = float(input("Cuanto escalar en x: "))
    scale_y = float(input("Cuanto escalar en y: "))
    # Crear una nueva imagen para almacenar el escalado
    scaled_img = np.zeros((int(1+round(x * scale_y)), int(1+round(y * scale_x))), dtype=np.uint8)
    # Aplicar el escalado
    for i in range(x):
        for j in range(y):
                    #orig_x = int(i * scale_y)
                    #orig_y = int(j * scale_x)
                    scaled_img[round(i*scale_x), round(j*scale_y)] = img[i, j]
    return scaled_img

def opcion (o,img,imgO):
    match o:
        case 1:
            return trasladar (img)
        case 2:
            return rotar(img)
        case 3:
            return escalar(img)
        case 4:
            return imgO
        case 5:
            return None
    
imgO = cv.imread("C:\\Users\\marce\\Downloads\\triforce.jpg",0)
img = imgO

i = 1
while img is not None:
    cv.imshow("imagen "+ str(i), img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    img = opcion(int(input("Como tranformar la imagen\n1.Trasladar\n2.Rotar\n3.Escalar\n4.Reiniciar imagen\n5.Terminar programa\n: ")),img, imgO)
    i=i+1
        

