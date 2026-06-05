import cv2 as cv 

rostro = cv.CascadeClassifier(r"C:\Users\marce\Downloads\haarcascade_frontalface_alt2.xml")
cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()
    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)
    for(x,y,w,h) in rostros:
        res = int((w+h)/8)
        img = cv.rectangle(img, (x,y), (x+w, y+h), (234, 23,23), 5)
        #cara =  img[y:y+h,x:x+w]
        ojos =  img[y+int(h*0.3):y+int(h*0.45),x+int(w*0.2):x+int(w*0.8)]
        boca =  img[y+int(h*0.7):y+int(h*0.9),x+int(w*0.3):x+int(w*0.7)]
        #cv.imshow('Cara', cara)
        cv.imshow('Ojos', ojos)
        cv.imshow('Boca', boca)
    cv.imshow('img', img)
    if cv.waitKey(1)== ord('q'):
        break
    
cap.release
cv.destroyAllWindows()