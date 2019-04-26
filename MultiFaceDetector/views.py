from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import requests
from io import BytesIO
import sqlite3
import face_recognition
import numpy as np
import io
from urllib.request import urlopen
import os
dirname = os.path.dirname(__file__)
dir = os.path.join(dirname, 'data\\img.jpg')
print(dir)
import sqlite3
def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

def MatchFaceData():
    #All the saved Encodings from Database are loaded into Saved_Encodings
    Saved_Encodings = []
    # All the saved Encodings from Database are loaded into Saved_Names
    Saved_Names = []
    # Creates a connection object KekaFaceRecognition Database
    conn = sqlite3.connect('db.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
    # Converts np.array to TEXT when inserting
    sqlite3.register_adapter(np.ndarray, adapt_array)
    # Converts TEXT to np.array when selecting
    sqlite3.register_converter("array", convert_array)
    cur = conn.cursor()
    for row in cur.execute("select FaceEncoding,EmployeeName from EmployeeFaceEncodings").fetchall():
        Saved_Encodings.append(row[0])
        Saved_Names.append(row[1])
    # Listing each face encoding from the frame
    face_encodings = []
    # List to keep track of names in the frame
    face_names = []
    image = face_recognition.load_image_file(dir)
    face_encodings = face_recognition.face_encodings(image)
    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        # Lesser the value lesse the tolerance(strict checking may cause recognition fail)
        matches = face_recognition.compare_faces(Saved_Encodings, face_encoding,tolerance = 0.43564)
        #print(matches)
        name = "Unknown"
        # If a match is found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = Saved_Names[first_match_index]     
        face_names.append(name)
    return face_names
import urllib.parse
import json
import base64
@csrf_exempt
def processImage(request):
    if(request.method == 'POST'):
        data = str(request.body,'utf-8')
        data = json.loads(data)
        imageData = base64.b64decode(data['imgData'])
        image_result = open(dir, 'wb')
        image_result.write(imageData)
        name = MatchFaceData()
        return HttpResponse(name)
    else:
        return HttpResponse("<b>A GET Request will not be processed</b>")
