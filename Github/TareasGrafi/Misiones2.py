import cv2 as cv
import numpy as np
import math

#Mision 1------------------------------------------------------------------------------------

img = cv.imread(r"C:\Users\marce\Downloads\m1_oscura_1.png", 0)
x, y = img.shape

trans_img = np.zeros((x, y), dtype=np.uint8)

for i in range(x):
    for j in range(y):
        trans_img[i][j] = img[i][j]*50


trans_img_cv2 = cv.add(trans_img,20)

cv.imwrite("m1_recuperado_x50.png", trans_img)
cv.imwrite("m1_recuperado_x50_mas20.png", trans_img_cv2)


#Mision 2------------------------------------------------------------------------------------

img2 = cv.imread(r"C:\Users\marce\Downloads\m2_mitad1_1.png", 0)

x, y = img2.shape

# Buscar coordenadas de los píxeles que no son blancos
coords = np.argwhere(img2 < 255)
fila_min, col_min = coords.min(axis=0)

    # trasladar para que ese punto quede en (0,0)
M_inversa = np.float32([[1, 0, -col_min], [0, 1, -fila_min]])
img2_or = cv.warpAffine(img2, M_inversa, (y, x))




img3 = cv.imread(r"C:\Users\marce\Downloads\m2_mitad2_1.png",0)
x, y = img3.shape
# 2. Definir el centro de rotación (mitad de la imagen)
centro = (y // 2, x // 2)

# 3. Obtener la matriz de rotación para 180 grados
# getRotationMatrix2D(centro, ángulo, escala)
matriz = cv.getRotationMatrix2D(centro, 180, 1.0)

# 4. Aplicar la rotación con warpAffine
img3_rotada = cv.warpAffine(img3, matriz, (y, x))

lienzo = np.full((400, 400, 3), 255, dtype=np.uint8)

for i in range(400):
    for j in range(400):
        if(i<200):
            lienzo[i][j] = img2_or[i][j]
        else:
            lienzo[i][j] = img3_rotada[i-200][j]


cv.imwrite("m2_qr_reconstruido.png", lienzo)

#Mision 3------------------------------------------------------------------------------------

img4 = np.zeros((600, 600, 3), dtype=np.uint8)
img4[:] = (40, 20, 20)

cv.circle(img4, (300,300), 170, (0,0,255), 3)
cv.circle(img4, (300,300), 110, (0,255,255), 2)
cv.rectangle(img4, (250, 260), (350, 340), (0,0,255), -1)
cv.line(img4, (0,0), (599,599), (255,255,255), 2)
cv.line(img4, (0,599), (599,0), (255,255,255), 2)
for i in range(8):
    angle = i * math.pi / 4
    x = int(300 + 140 * math.cos(angle))
    y = int(300 + 140 * math.sin(angle))
    cv.circle(img4, (x, y), 8, (0, 255, 0), -1)

cv.putText(img4, "SECTOR-9", (140, 560), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)

cv.imwrite("m3_sello_forjado_v2.png", img4)

#Mision 4--------------------------------------------------------------------------------------

img5 = cv.imread(r"C:\Users\marce\Downloads\m4_ruido_1.png")

kernel = np.ones((3, 3), np.float32) / 9
img_suavizada = cv.filter2D(img5, -1, kernel)

cv.imwrite("m4_suavizada.png", img_suavizada)

img_hsv = cv.cvtColor(img_suavizada, cv.COLOR_BGR2HSV)

#Definir los límites para segmentar el color Cyan (Hue ~ 90)
lower_cyan = np.array([85, 50, 50])  # Ajuste según el rango de cian
upper_cyan = np.array([95, 255, 255])

mask_cyan = cv.inRange(img_hsv, lower_cyan, upper_cyan)

cv.imwrite("m4_mask_cyan.png", mask_cyan)

#Mision 5--------------------------------------------------------------------------------------



'''cv.imshow("m1_oscura", img)
cv.imshow("m1_recuperado_x50", trans_img)
cv.imshow("m1_recuperado_x50_mas20", trans_img_cv2)

cv.imshow("img2", img2)
cv.imshow("img2_or", img2_or)
cv.imshow("img3", img3)
cv.imshow("img3_rotada", img3_rotada)
cv.imshow("m2_qr_reconstruido", lienzo)

cv.imshow("m3_sello_forjado_v2", img4)

cv.imshow("Imagen Suavizada", img_suavizada)
cv.imshow("Mascara Cyan", mask_cyan)'''

cv.waitKey(0)
cv.destroyAllWindows()