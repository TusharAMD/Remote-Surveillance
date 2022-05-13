import os
import flask
from flask import request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from time import sleep
import pymongo
from flask_cors import CORS,cross_origin

app = flask.Flask(__name__)
CORS(app)
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.wonbr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mgdb = client["visitordb"]
coll = mgdb["visitors"]

@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp():
    if request.method == "POST":
        global db
        
        command = str(request.form["Body"]).lower()
        status_ref = db.collection(u'motor_status').document(u'curr_status')
        if command == "open":
            #firebase update
            
            status_ref.update({u'value': True})
            sleep(5)
            status_ref.update({u'value': False})
            ###
        elif command == "close":
            #firebase update
            status_ref.update({u'value': False})
            ###
    else:
        pass
    return {"status":200}

@cross_origin()
@app.route('/getDatabase', methods=['GET', 'POST'])
def getDatabase():
    global coll
    if request.method == "GET":
        retDict = {"data":[]}
        allDocs = coll.find()
        for ele in allDocs:
            print(ele)
            del ele["_id"]
            retDict["data"].append(ele)
    return retDict
if __name__ == "__main__":
    app.run(port=5000, debug=True)