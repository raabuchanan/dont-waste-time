import httplib, urllib, base64, json

import time

headers = {
    # Request headers.
    'Content-Type': 'application/json',

    # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
    'Ocp-Apim-Subscription-Key': '69766cdb74e748cd9266eb53fae6316f',
}

# Replace 'examplegroupid' with an ID you haven't used for creating a group before.
# The valid characters for the ID include numbers, English letters in lower case, '-' and '_'. 
# The maximum length of the ID is 64.
personGroupId = 'patients'

personId = '60bace47-d012-4f1e-9e01-e852e3311791'



#################################################################################
#               DELETE GROUP
##################################################################################


# The userData field is optional. The size limit for it is 16KB.
body = "{ 'name':'group1', 'userData':'user-provided data attached to the person group' }"
conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
conn.request("DELETE", "/face/v1.0/persongroups/%s" % personGroupId, body, headers)
response = conn.getresponse()
data = response.read()
print(data)
conn.close()


#################################################################################
#               CREATE GROUP
##################################################################################

conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
conn.request("PUT", "/face/v1.0/persongroups/%s" % personGroupId, body, headers)
response = conn.getresponse()
print(response.reason)
conn.close()



#################################################################################
#               CREATE PERSON IN GROUP
##################################################################################

body = "{ 'name':'Russell', 'userData':'%s'}" % "test"

conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')

conn.request("POST", "/face/v1.0/persongroups/%s/persons?" % personGroupId, body, headers)
response = conn.getresponse()
data = json.loads(response.read())
print(data)
personId = str(data['personId'])
conn.close()



#################################################################################
#               GET PERSON FROM GROUP
##################################################################################

conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')

conn.request("GET", "/face/v1.0/persongroups/%s/persons/%s?" % (personGroupId, personId), body, headers)
response = conn.getresponse()
data = response.read()
print(data)
conn.close()




#################################################################################
#               ADD PICTURE TO PERSON
##################################################################################


headers['Content-Type'] = 'application/octet-stream'
filename = '/home/raab/russell1.jpg'
f = open(filename, "rb")
body = f.read()
f.close()

conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
string = "/face/v1.0/persongroups/%s/persons/%s/persistedFaces?" % (personGroupId, personId)
conn.request("POST", string, body, headers)
response = conn.getresponse("")
data = json.loads(response.read())
print(data)
conn.close()




#################################################################################
#               GET PICTURE FROM PERSON
##################################################################################
persistedFaceId = data['persistedFaceId']

body = "{ 'name':'Russell', 'userData':'%s'}" % "test"

conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
conn.request("GET", "/face/v1.0/persongroups/%s/persons/%s/persistedFaces/%s?" % (personGroupId, personId, persistedFaceId), body, headers)
response = conn.getresponse()
data = response.read()
print(data)
conn.close()


#################################################################################
#               TRAIN GROUP ON IMAGES
##################################################################################

params = urllib.urlencode({
})
headers = {
    # Request headers.
    'Content-Type': 'application/json',

    # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
    'Ocp-Apim-Subscription-Key': '69766cdb74e748cd9266eb53fae6316f',
}

conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
conn.request("POST", "/face/v1.0/persongroups/%s/train?" % (personGroupId), params, headers)
response = conn.getresponse()
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
data = response.read()
print(data)
conn.close()



#################################################################################
#               ANALYSE NEW QUERY IMAGE
##################################################################################

params = urllib.urlencode({
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
})

headers['Content-Type'] = 'application/octet-stream'
filename = '/home/raab/russell1.jpg'
f = open(filename, "rb")
body = f.read()
f.close()



conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
response = conn.getresponse()
data = json.loads(response.read())
print(data)
print(data[0])
faceID = data[0]['faceId']

conn.close()


#################################################################################
#               COMPARE QUERY IMAGE TO GROUP
##################################################################################

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '69766cdb74e748cd9266eb53fae6316f',
}

params = urllib.urlencode({
})

body = str({

    "personGroupId":str(personGroupId),
    "faceIds":[str(faceID)],
    "maxNumOfCandidatesReturned":1,
    "confidenceThreshold": 0.5

})

print("Here")
time.sleep(3)
conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print("/face/v1.0/identify?%s" % params, body, headers)
conn.request("POST", "/face/v1.0/identify?%s" % params, body, headers)
response = conn.getresponse()
data = response.read()
print(data)
conn.close()