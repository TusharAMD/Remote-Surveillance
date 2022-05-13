import numpy as np
import face_recognition
import cv2

vid = cv2.VideoCapture(0)
name = input("Enter Your Name: ")
while(True):
    _,image_unknown = vid.read()
    #image_unknown = cv2.imread("verified-database/mark.jpg") 
    cv2.imshow('frame',image_unknown)
    if face_recognition.face_encodings(image_unknown):
        print("Face Detected")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        try:
            imguk_encoding = face_recognition.face_encodings(image_unknown)[0]
            print(imguk_encoding)
            cv2.imwrite(f"verified-database/{name}.jpg",image_unknown)
            f = open(f"verified-database/{name}.txt","w")
            f.write(str(imguk_encoding))
            f.close()
            break
        except:
            pass