from flask import Flask, jsonify, session
from flask import render_template, request, redirect, url_for

import httplib, urllib, base64, json
import time
import numpy as np
import cv2
import argparse
import operator
import os


subscription_id = '78836ad0eb164298ac473d98449a1c43'
#subscription_id = '69766cdb74e748cd9266eb53fae6316f'
image = "static/images/default.jpg"
personGroupId = 'patients'

our_database = []

detected_emotions = {}
glasses = ""
detected_age = ""
detected_gender = ""
health_care_provider = ""
uuid = ""

class FaceMatcher:


    def __init__ (self):
        self.headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': subscription_id,
        }

    def create_group(self):
        conn = httplib.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        body = "{ 'name':'group1', 'userData':'user-provided data attached to the person group' }"
        conn.request("PUT", "/face/v1.0/persongroups/%s" % personGroupId, body, self.headers)
        response = conn.getresponse()
        conn.close()
        print("Creating Group: %s" % response.reason)


    def delete_group(self):
        conn = httplib.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        body = "{ 'name':'group1', 'userData':'user-provided data attached to the person group' }"
        conn.request("DELETE", "/face/v1.0/persongroups/%s" % personGroupId, body, self.headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        print("Deleting Group: %s" % response.reason)


    def add_person(self, filename):
        conn = httplib.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        body = "{ 'name':'%s', 'userData':'test'}" % filename
        conn.request("POST", "/face/v1.0/persongroups/%s/persons?" % personGroupId, body, self.headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        personId = str(data['personId'])


        conn.close()
        print("Adding Person: %s" % response.reason)

        return personId


    def add_picture(self, picture, personId):
        conn = httplib.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        self.headers['Content-Type'] = 'application/octet-stream'
        print(picture)
        filename = picture
        f = open(filename, "rb")
        body = f.read()
        f.close()

        conn.request("POST", "/face/v1.0/persongroups/%s/persons/%s/persistedFaces?" % (personGroupId, personId), body, self.headers)
        response = conn.getresponse("")
        data = json.loads(response.read())
        self.headers['Content-Type'] = 'application/json'
        conn.close()
        print("Adding Picture: %s" % response.reason)


    def train_group(self):
        conn = httplib.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        params = urllib.urlencode({
        })

        conn.request("POST", "/face/v1.0/persongroups/%s/train?" % (personGroupId), params, self.headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()



    def analyze_image(self):
        global image, detected_emotions, glasses, detected_age, detected_gender, health_care_provider, uuid
        conn = httplib.HTTPSConnection('westeurope.api.cognitive.microsoft.com')

        params = urllib.urlencode({
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
        })

        self.headers['Content-Type'] = 'application/octet-stream'
        filename = 'static/image.jpg'
        f = open(filename, "rb")
        body = f.read()
        f.close()


        conn.request("POST", "/face/v1.0/detect?%s" % params, body, self.headers)
        response = conn.getresponse()
        data = json.loads(response.read())

        if 'faceId' not in data[0]:
            print(data)
        else:
            faceId = data[0]['faceId']

        detected_age = data[0]['faceAttributes']['age']
        detected_gender = data[0]['faceAttributes']['gender']

        glasses = data[0]['faceAttributes']['glasses']

        detected_emotions = data[0]['faceAttributes']['emotion']

        

        self.headers['Content-Type'] = 'application/json'



        params = urllib.urlencode({})

        body = str({

            "personGroupId":str(personGroupId),
            "faceIds":[str(faceId)],
            "maxNumOfCandidatesReturned":1,
            "confidenceThreshold": 0.5

        })

        conn.request("POST", "/face/v1.0/identify?%s" % params, body, self.headers)
        response = conn.getresponse()
        data = json.loads(response.read())

        conn.close()

        print(data)
        if(len(data[0]['candidates']) > 0):

            for candidate in data[0]['candidates']:
                personId = candidate['personId']

                indir = '/home/raab/DontWasteTIme/voiceflask/static/files'
                for root, dirs, filenames in os.walk(indir):

                    for filename in filenames:

                        with open(os.path.join(root,filename)) as fd:
                            medical_data = json.load(fd)

                        
                        if personId == medical_data['personID']:

                            name = filename.split('.')[0]

                            print("Found Match: %s, %s" % (name, candidate['confidence']))

                            image = "static/images/" + name + "1.jpg"

                            health_care_provider = medical_data['entry'][0]['resource']['name']

                            uuid = medical_data['entry'][0]['resource']['id']

        else:
            print("No Match")


        if health_care_provider == "":
            health_care_provider = "NO RECORD FOUND"

        if uuid == "":
            uuid = "NO RECORD FOUND"


app = Flask(__name__, static_url_path='/static')

@app.route("/c/", methods=['GET'])
def search():
    keyword = request.args.get('q')
    keyword = clean_keyword(keyword)
    page = request.args.get('p')

@app.route("/", methods=['GET'])
def home():
    global image, detected_emotions, glasses, detected_age, detected_gender, health_care_provider, uuid
    
    return render_template("Sample.html", image=image, detected_emotions=detected_emotions, glasses=glasses,detected_age=detected_age,
detected_gender=detected_gender,health_care_provider=health_care_provider, uuid=uuid)

@app.route("/reset", methods=['POST'])
def reset():
    print "reset!"
    last_offset = 0
    return 

last_offset = 0
recording = False

@app.route("/", methods=['POST'])
def receive():
    global recording
    global last_offset

    j = request.get_json()
    for i in j:
        if i['Offset'] > last_offset and 'DisplayText' in i:
            dt = i['DisplayText']
            if dt == "Start.":
                recording = True
                print "start recording..."
            elif dt == "Stop.":
                recording = False
                print "stop recording..."
            if recording:
                print dt
            last_offset = i['Offset']
    return render_template("Sample.html")

if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument('--demo', action='store_true')
    parser.add_argument('--train', action='store_true')
    args = parser.parse_args()


    matcher = FaceMatcher()


    if args.train:
        matcher.delete_group()
        matcher.create_group()


        indir = '/home/raab/DontWasteTIme/voiceflask/static/files'
        for root, dirs, filenames in os.walk(indir):


            for filename in filenames:
                print(filename)

                with open(os.path.join(root,filename)) as fd:
                    medical_data = json.load(fd)

                name = filename.split('.')[0]
                personId = matcher.add_person(name)

                matcher.add_picture('static/images/' + name + '1.jpg', personId)
                matcher.add_picture('static/images/' + name + '2.jpg', personId)
                matcher.add_picture('static/images/' + name + '3.jpg', personId)


                medical_data['personID'] = personId



                with open(os.path.join(root,filename), 'w') as outfile:
                    json.dump(medical_data, outfile)


        matcher.train_group()

    else:


        cap = cv2.VideoCapture(0)

        ret, frame = cap.read()

        cv2.imwrite( "static/image.jpg", frame );

        
        cap.release()
        cv2.destroyAllWindows()

        matcher.analyze_image()


        app.run(host='0.0.0.0', port=80, debug=True)


