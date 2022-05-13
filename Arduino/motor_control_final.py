from pyfirmata import Arduino, SERVO, util
from time import sleep
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

print("Starting...")
port = 'COM4'
pin = 9
pin_down = 10
board = Arduino(port)

board.digital[pin].mode = SERVO
board.digital[pin_down].mode = SERVO

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
print("db connected")
board.digital[pin_down].write(90)

def rotateservo(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.015)

def rotateservo_down(pin_down, angle):
    board.digital[pin_down].write(angle)
    sleep(0.5)
    board.digital[pin_down].write(90)
    
    

li = [0,0]
while True:
    status = db.collection('motor_status').get()
    #print(status[0])
    #print(status[0].to_dict()['value'])
    li.append(status[0].to_dict()['value'])
    #x = input("input: ")
    if status[0].to_dict()['value']==True and li[len(li)-1]!=li[len(li)-2]:
        rotateservo(pin, 90)
        print(f"Value Changed to {print(status[0].to_dict()['value'])}")
        print("Now Opening")
        sleep(2)
        rotateservo_down(pin_down, 61)
        
    elif status[0].to_dict()['value']==False and li[len(li)-1]!=li[len(li)-2]:
        rotateservo_down(pin_down, 130)
        sleep(2)
        rotateservo(pin, 0)
        print(f"Value Changed to {print(status[0].to_dict()['value'])}")
        print("Now Closing")
