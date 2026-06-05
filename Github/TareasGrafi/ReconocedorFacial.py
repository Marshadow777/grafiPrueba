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
        #img = cv.rectangle(img, (x,int(y+h/2)), (x+w, y+h), (0,255,0),5 )
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)) , 21, (0, 0, 0), 2 )
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)) , 21, (0, 0, 0), 2 )

        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)) , 20, (255, 255, 255), -1 )
        img = cv.line(img, (x+int(w*0.25), y+int(h*0.28)), (x+int(w*0.4), y+int(h*0.38)), (0,0,0), 15)

        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)) , 20, (255, 255, 255), -1 )
        img = cv.line(img, (x+int(w*0.75), y+int(h*0.28)), (x+int(w*0.6), y+int(h*0.38)), (0,0,0), 15)

        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)) , 5, (0, 255, 0), -1 )
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)) , 5, (0, 255, 0), -1 )
        #img = cv.rectangle(img, (x+10,y+10), (x+w, y+h), (234,0 ,234), 5)
        img = cv.circle(img, (x + int(w*0.45), y + int(h*0.65)) , 20, (55, 78, 111), -1)
        img = cv.circle(img, (x + int(w*0.55), y + int(h*0.65)) , 20, (55, 78, 111), -1)
        img = cv.circle(img, (x + int(w*0.35), y + int(h*0.62)) , 20, (55, 78, 111), -1)
        img = cv.circle(img, (x + int(w*0.65), y + int(h*0.62)) , 20, (55, 78, 111), -1)

        img = cv.circle(img, (x + int(w*0.5), y + int(h*0.55)) , 25, (0,0,255), -1)

        img = cv.rectangle(img, (x,y+int(h*0.4)),(x + int(w*0.1),y+int(h*0.6)), (255,255,0), -1)
        img = cv.rectangle(img, (x+w,y+int(h*0.4)),(x + int(w*0.9),y+int(h*0.6)), (255,255,0), -1)
        #img2=  img[y:y+h,x:x+w]
        #cv.imshow('img2', img2)
    cv.imshow('img', img)
    if cv.waitKey(1)== ord('q'):
        break
    
cap.release
cv.destroyAllWindows()