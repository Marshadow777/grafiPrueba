
import cv2 as cv
import numpy as np
import math

# Cargar la imagen
img = cv.imread(r"C:\Users\marce\Downloads\Ovni.png", 0)
qr = cv.imread(r"C:\Users\marce\Downloads\qr.png", 0)
img_microfilm = cv.imread(r"C:\Users\marce\Downloads\text.png", 0)
x, y = img.shape
rows, cols = img.shape

# ==========================================
# MÉTODO 1: MODO RAW (Manipulación de Píxeles)
# ==========================================
# 1. Crea un lienzo negro vacío (np.zeros) de 600x800
# 2. Mueve los píxeles al nuevo lienzo sumando 300 en X y 200 en Y
# Definir el desplazamiento en x e y
dx = 250
dy = 250

    
# Crear una imagen vacía para la traslación
translated_img = np.zeros((x, y), dtype=np.uint8)

    # Trasladar la imagen
for i in range(x):
        for j in range(y):
            new_x = i + dx
            new_y = j + dy
            if 0 <= new_x and 0 <= new_y and new_x<x and new_y<y:
                translated_img[new_x, new_y] = img[i, j]


# ==========================================
# MÉTODO 2: MODO OPENCV (Matriz de Transformación)
# ==========================================
# 1. Crea la matriz de traslación 'M' en NumPy
# 2. Aplica cv2.warpAffine a la imagen original
M = np.float32([[1, 0, 250], [0, 1, 250]])
dst = cv.warpAffine(img, M, (cols, rows))

# ==========================================
# MÉTODO 1: MODO RAW (Trigonometría)
# ==========================================
# 1. Crea un lienzo vacío de 500x500
# 2. Usa las fórmulas de senos y cosenos para mapear los píxeles (¡Cuidado con los huecos negros si mapeas hacia adelante!)
x , y = qr.shape

diag = 10 + round(math.sqrt((x*x)+(y*y)))
rotated_img = np.zeros((x, y), dtype=np.uint8)

cx, cy = int(x  // 2), int(y  // 2)
angle = 45
theta = math.radians(angle)


    # Rotar la imagen
for i in range(x):
        for j in range(y):
            new_x = int((j - cx) * math.cos(theta) - (i - cy) * math.sin(theta) + cx)
            new_y = int((j - cx) * math.sin(theta) + (i - cy) * math.cos(theta) + cy)  #round((diag//2))
            if 0 <= new_x < x and 0 <= new_y < y:
                rotated_img[new_y, new_x] = qr[i, j]

# ==========================================
# MÉTODO 2: MODO OPENCV
# ==========================================
# 1. Obtén la matriz con cv2.getRotationMatrix2D
# 2. Aplica cv2.warpAffine

rows, cols = qr.shape
center = (cols / 2, rows / 2)
M = cv.getRotationMatrix2D(center, -45, 1)
dstR = cv.warpAffine(qr, M, (cols, rows))

recorte = img_microfilm[700:900, 700:900]

# ==========================================
# MÉTODO 1: MODO RAW (Vecino más cercano manual)
# ==========================================
# 1. Crea un lienzo 5 veces más grande que el recorte
# 2. Multiplica las coordenadas para mapear los colores
x, y = recorte.shape
    # Definir el factor de escala
scale_x = 5
scale_y = 5
    # Crear una nueva imagen para almacenar el escalado
scaled_img = np.zeros((int(1+round(x * scale_y)), int(1+round(y * scale_x))), dtype=np.uint8)
    # Aplicar el escalado
for i in range(x):
        for j in range(y):
                    #orig_x = int(i * scale_y)
                    #orig_y = int(j * scale_x)
                    scaled_img[round(i*scale_x), round(j*scale_y)] = recorte[i, j]

# ==========================================
# MÉTODO 2: MODO OPENCV (Interpolación)
# ==========================================
# 1. Usa cv2.resize con fx=5, fy=5 e interpolation=cv2.INTER_CUBIC
x,y = recorte.shape[:5]
alto, ancho = recorte.shape[:5]
M = np.float32([[scale_x, 0, 0], [0, scale_y, 0]])
imagen_escalada = cv.warpAffine(recorte, M, (int(ancho * scale_x), int(alto * scale_y)))
new_dimensions = (int(ancho * scale_x), int(alto * scale_y))
img_resized = cv.resize(imagen_escalada, new_dimensions, interpolation=cv.INTER_CUBIC)


cv.imshow("Imagen", img)
cv.imshow("Centro", translated_img)
cv.imshow("CentroCv2", dst)
cv.imshow("Qr", qr)
cv.imshow("Rotacion", rotated_img)
cv.imshow("RotacionCv2", dstR)
cv.imshow("texto", img_microfilm)
cv.imshow("Escalado", scaled_img)
cv.imshow("EscaladoCv2", img_resized)
cv.waitKey(0)
cv.destroyAllWindows()