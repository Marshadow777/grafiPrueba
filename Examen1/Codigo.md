#  Reporte de Misión: Graficación Táctica
**Agente Especial:** [Marcelo Vicente Pascual Tapia/24121386]

---
##  Evidencias de Misión
### Código
```
import cv2 as cv
import numpy as np

img = cv.imread(r"C:\Users\marce\Downloads\m1_oscura.png", 0)
x,y = img.shape

mensaje = np.zeros((x, y), dtype=np.uint8)

for i in range(x):
    for j in range(y):
        if 1<=img[i][j]<=5:
            mensaje[i][j]=img[i][j]*50


mensajeCv = np.zeros((x, y), dtype=np.uint8)
mensajeCv = cv.multiply(img, 100)

cv.imshow("Original", img)
cv.imshow("Mensaje", mensaje)
cv.imshow("MensajeCv", mensajeCv)
cv.waitKey(0)
cv.destroyAllWindows()

mitad1 = cv.imread(r"C:\Users\marce\Downloads\m2_mitad1.png", 0)
mitad2 = cv.imread(r"C:\Users\marce\Downloads\m2_mitad2.png", 0)
rows, cols = mitad2.shape

qr = np.zeros((400,400), dtype=np.uint8)

center = (cols / 2, rows / 2)
M = cv.getRotationMatrix2D(center, 180, 1)
mitad2R = cv.warpAffine(mitad2, M, (cols, rows))

for i in range(400):
    for j in range(400):
        if i<200:
            qr[i][j] = mitad1[i][j]
        else:
            qr[i][j] = mitad2R[i-200][j]

cv.imshow("Resultado", qr)
cv.waitKey(0)
cv.destroyAllWindows()


sello = np.full((500, 500, 3), (50, 20, 20), dtype=np.uint8)

cv.circle(sello, (250,250), 100, (33,222,255), 3)
cv.rectangle(sello, (200,200), (300,300), (0,0,255), -1)
cv.line(sello, (0,0), (499,499), (255,255,255), 2)
cv.line(sello, (499,0), (0,499), (255,255,255), 2)

cv.imshow("Sello", sello)
cv.waitKey(0)
cv.destroyAllWindows()


contrasena = cv.imread(r"C:\Users\marce\Downloads\m4_ruido.png")
hsv = cv.cvtColor(contrasena,cv.COLOR_BGR2HSV)

lower_cian = np.array([80, 100, 100])  
upper_cian = np.array([100, 255, 255])  

masc = cv.inRange(hsv, lower_cian, upper_cian)
result = cv.bitwise_and(contrasena, contrasena, mask=masc)

cv.imshow("Password", result)
cv.waitKey(0)
cv.destroyAllWindows()
```



---
##  Análisis del Analista (Reflexiones Finales)

1. **Sobre los Operadores Puntuales (Misión 1):** Matemáticamente, ¿qué pasaría si en lugar de multiplicar por 50, hubieras sumado 50 a cada píxel oscuro? ¿Se revelaría el texto igual de claro o la imagen perdería contraste?
> *[Escribe tu respuesta aquí]*

2. **Sobre el Espacio HSV (Misión 4):** ¿Por qué el modelo de color BGR es ineficiente para la Recuperación de Información cuando buscamos "todos los tonos de azul celeste", y por qué el modelo HSV resuelve este problema con una sola variable?
> *[Escribe tu respuesta aquí]*

3. **Sobre Ecuaciones Paramétricas (Misión 5):** ¿Por qué las ecuaciones paramétricas (usando el parámetro t) son mejores para dibujar formas cerradas y complejas en graficación por computadora que usar la clásica función $y=f(x)$?
> *[Escribe tu respuesta aquí]*


