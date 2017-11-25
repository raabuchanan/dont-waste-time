#!/usr/bin/env python

import httplib, urllib, base64, json
import time
import numpy as np
import cv2
import argparse


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
        filename = 'image.jpg'
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
        filename = 'image.jpg'
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
    


    parser = argparse.ArgumentParser()
    parser.add_argument('--demo', action='store_true')
    parser.add_argument('--train', action='store_true')
    args = parser.parse_args()


    matcher = FaceMatcher()


    if args.demo:

        cap = cv2.VideoCapture(0)

        # while(True):
            # Capture frame-by-frame
        ret, frame = cap.read()

        cv2.imwrite( "image.jpg", frame );

            # np_frame = np.asarray(frame)
            # print(np.shape)

            # # Display the resulting frame
            # cv2.imshow('frame',frame)
            # if cv2.waitKey(1000) & 0xFF == ord('q'):
            #     break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

        matcher.analyze_image()

    elif args.train:



    

        matcher.delete_group()
        matcher.create_group()

        matcher.add_person()

        matcher.add_picture()


        matcher.train_group()

    


    else:


    

        matcher.delete_group()
        matcher.create_group()

        matcher.add_person()

        matcher.add_picture()


        matcher.train_group()

        matcher.analyze_image()