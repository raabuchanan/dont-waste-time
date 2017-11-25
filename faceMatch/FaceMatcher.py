#!/usr/bin/env python

import httplib, urllib, base64, json
import time

subscription_id = '69766cdb74e748cd9266eb53fae6316f'

personGroupId = 'patients'

class FaceMatcher:


    def __init__ (self):
        self.personId = ""

        self.headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': subscription_id,
        }

    def create_group(self):
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        body = "{ 'name':'group1', 'userData':'user-provided data attached to the person group' }"
        conn.request("PUT", "/face/v1.0/persongroups/%s" % personGroupId, body, self.headers)
        response = conn.getresponse()
        conn.close()
        print("Creating Group: %s" % response.reason)


    def delete_group(self):
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        body = "{ 'name':'group1', 'userData':'user-provided data attached to the person group' }"
        conn.request("DELETE", "/face/v1.0/persongroups/%s" % personGroupId, body, self.headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        print("Deleting Group: %s" % response.reason)


    def add_person(self):
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        body = "{ 'name':'Russell', 'userData':'test'}"
        conn.request("POST", "/face/v1.0/persongroups/%s/persons?" % personGroupId, body, self.headers)
        time.sleep(1)
        response = conn.getresponse()
        data = json.loads(response.read())
        self.personId = str(data['personId'])
        conn.close()
        print("Adding Person: %s" % response.reason)


    def add_picture(self):
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        self.headers['Content-Type'] = 'application/octet-stream'
        filename = '/home/raab/russell1.jpg'
        f = open(filename, "rb")
        body = f.read()
        f.close()

        conn.request("POST", "/face/v1.0/persongroups/%s/persons/%s/persistedFaces?" % (personGroupId, self.personId), body, self.headers)
        response = conn.getresponse("")
        data = json.loads(response.read())
        self.headers['Content-Type'] = 'application/json'
        conn.close()
        print("Adding Picture: %s" % response.reason)


    def train_group(self):
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        params = urllib.urlencode({
        })

        conn.request("POST", "/face/v1.0/persongroups/%s/train?" % (personGroupId), params, self.headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()



    def analyze_image(self):
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')

        params = urllib.urlencode({
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
        })

        self.headers['Content-Type'] = 'application/octet-stream'
        filename = '/home/raab/russell1.jpg'
        f = open(filename, "rb")
        body = f.read()
        f.close()


        conn.request("POST", "/face/v1.0/detect?%s" % params, body, self.headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        faceID = data[0]['faceId']

        self.headers['Content-Type'] = 'application/json'



        params = urllib.urlencode({
        })

        body = str({

            "personGroupId":str(personGroupId),
            "faceIds":[str(faceID)],
            "maxNumOfCandidatesReturned":1,
            "confidenceThreshold": 0.5

        })

        conn.request("POST", "/face/v1.0/identify?%s" % params, body, self.headers)
        response = conn.getresponse()
        data = response.read()
        print(data)


        conn.close()



if __name__ == "__main__":
    

    matcher = FaceMatcher()


    matcher.delete_group()
    matcher.create_group()

    matcher.add_person()

    matcher.add_picture()


    matcher.train_group()

    matcher.analyze_image()