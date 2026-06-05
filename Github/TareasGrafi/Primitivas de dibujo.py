import cv2
import numpy as np

img = np.ones((500, 500, 3), dtype="uint8")*255

# cv2.circle(imagen, centro, radio, color, grosor)
cv2.circle(img, (150, 150), 100, 	(28, 27, 23), -1) # cabeza
cv2.circle(img, (215,150), 40, 	(255,255,255), -1) #boca
cv2.circle(img, (215, 50), 40, 	(28, 27, 23), -1) #nariz
cv2.circle(img, (330, 150), 40, (28, 27, 23), -1) #mano
cv2.circle(img, (190, 260), 40, (28, 27, 23), -1) #pecho
cv2.line(img, (190, 270), (330, 150), (28, 27, 23), 17) #brazo
cv2.circle(img, (230, 350), 56, (28, 27, 23), -1) #estomago
cv2.circle(img, (50, 300), 40, (28, 27, 23), -1) #mano 2
cv2.line(img, (50, 320), (130, 310), (28, 27, 23), 17) #brazo 2
cv2.line(img, (190, 200), (130, 310), (28, 27, 23), 17) #brazo 3
cv2.rectangle(img, (176, 260), (230, 350), (28, 27, 23), -1) #costillas
cv2.line(img, (190, 260), (247, 350), (28, 27, 23), 80) #curvas
cv2.line(img, (240, 370), (140, 400), (28, 27, 23), 17) #pierna Iz
cv2.line(img, (150, 450), (140, 400), (28, 27, 23), 17) #pierna Iz 2
cv2.circle(img, (145, 460), 30, (28, 27, 23), -1) #talon Iz 
cv2.circle(img, (105, 460), 35, (28, 27, 23), -1) #pata Iz 
cv2.line(img, (150, 438), (105, 435), (28, 27, 23), 17) #empeine Iz
cv2.line(img, (150, 480), (105, 486), (28, 27, 23), 17) #suela Iz
cv2.line(img, (260, 380), (330, 305), (28, 27, 23), 17) #pierna De
cv2.line(img, (380, 350), (330, 305), (28, 27, 23), 17) #pierna De 2
cv2.circle(img, (390, 344), 30, (28, 27, 23), -1) #talon De
cv2.circle(img, (415, 300), 35, (28, 27, 23), -1) #pata De
cv2.line(img, (370, 344), (391, 290), (28, 27, 23), 17) #empeine De
cv2.line(img, (408, 355), (440, 309), (28, 27, 23), 17) #suela De
# cv2.putText(imagen, texto, org, fuente, escala, color, grosor)
#cv2.putText(img, 'Hola OpenCV', (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

cv2.imshow("Imagen", img)
cv2.waitKey(0)
cv2.destroyAllWindows