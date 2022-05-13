import cv2
import numpy as np
import face_recognition
import glob
import re
import pyttsx3  
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from time import sleep
import vlc
import gtts
import time
import os
import pymongo
import base64
import requests
import datetime
from twilio.rest import Client 
import inspect

engine = pyttsx3.init()  


files = glob.glob("verified-database/*.txt")

#Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
##

#MongoDB
client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.wonbr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mgdb = client["visitordb"]
coll = mgdb["visitors"]
##

#Twilio Send Message for Unknown
account_sid = 'AC9807e8964cc05794c3de4f37c190247b' 
auth_token = '2d99afd5f8e26183b87387778a2d3c2d' 
client = Client(account_sid, auth_token) 
##


vid = cv2.VideoCapture(0)
while(True):
    _,image_unknown = vid.read()
    cv2.imshow('frame',image_unknown)
    
    k = cv2.waitKey(1)
 
    if k == 99:
        if face_recognition.face_encodings(image_unknown):
            print("Face Detected")
            
            ##ImgBB##
            cv2.imwrite("face.png",image_unknown)
            with open("face.png", "rb") as file:
                url = "https://api.imgbb.com/1/upload"
                payload = {
                    "key": "fb13020baf1e55ab0f8abe7be3834531",
                    "image": base64.b64encode(file.read()),
                }
                res = requests.post(url, payload)
                url = res.json()["data"]["url"]

            ##MongoDB Insert
            tempdict = {"key":"Unknown","imageurl":url,"date":datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")}
            coll.insert_one(tempdict)
            ###
            
            
        else:
            print("No Face Detected")
        try:
            imguk_encoding = face_recognition.face_encodings(image_unknown)[0]
            for file in files:
                #print(file)
                f = open(file,"r")
                a = f.read()
                a = a.replace('\n' , ' ')
                a = a.replace('[' , '')
                a = a.replace(']' , ' ')
                b = a.split(" ")
                li = []
                #print(b)
                for i in range(len(b)):
                    try:
                       li.append(float(b[i]))
                    except:
                        pass
                #print(li)
                start = file.index("\\")
                end = file.index(".")
                name = file[start+1:end]
                results = face_recognition.compare_faces([li],imguk_encoding)
                
            if results[0]:
            
                #firebase update
                status_ref = db.collection(u'motor_status').document(u'curr_status')
                status_ref.update({u'value': True})
                
                sleep(5)
                status_ref.update({u'value': False})
                ###
                ##MongoDB update
                myquery = { "imageurl": url }
                newvalues = { "$set": { "key": name } }
                coll.update_one(myquery, newvalues)
                ##
            
                print(f"Welcome {name}")
                gtts.gTTS(f"Welcome {name}").save("welcome.mp3")
                
                '''p = vlc.MediaPlayer(".\welcome.mp3")
                p.play()
                time.sleep(0.5)
                while p.is_playing():
                    time.sleep(0.5) 
                break'''
                os.system("python runWelcome.py")
                
            
            ## Send Message on Whatsapp if user not in Database##
            if True not in results:
                print("Unknown Face")
                message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body='Hey there!! A unknown person is trying to enter. If you wish to open the door type OPEN',
                              media_url=f"{url}",
                              to='whatsapp:+919324133348' 
                          ) 
        except Exception as e:
            print(e)
            pass
