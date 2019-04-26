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
import cv2
from urllib.request import urlopen
face_cascade = cv2.CascadeClassifier('C:\\Users\\manohar.k\\source\\repos\\KekaHr\\KekaHr\\MultiFaceDetector\\templates\\haarcascade_frontalface_default.xml')
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
    Max_Tries = 2
    Tries = 0
    NoMatch = True
    tolerance_tweak = 0.4
    name  = 'NA'
    while Tries != Max_Tries:
        framehere = cv2.imread("C:\\Users\\manohar.k\\source\\repos\\KekaHr\\KekaHr\\MultiFaceDetector\\data\\img.jpg")
        faces = face_cascade.detectMultiScale(framehere,1.3)
        if len(faces)>=1:
            face = face_recognition.load_image_file("C:\\Users\\manohar.k\\source\\repos\\KekaHr\\KekaHr\\MultiFaceDetector\\data\\img.jpg")
            NewEncoding = face_recognition.face_encodings(face)[0]
            try:
                conn = sqlite3.connect('db.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
                sqlite3.register_adapter(np.ndarray, adapt_array)
                sqlite3.register_converter("array", convert_array)
                cur = conn.cursor()
                for row in cur.execute("select FaceEncoding,EmployeeName from EmployeeFaceEncodings").fetchall():
                    SavedEncoding = row[0]
                    matched = face_recognition.compare_faces([NewEncoding],SavedEncoding,tolerance = tolerance_tweak)
                    if matched[0]:
                        NoMatch = False
                        Tries = Max_Tries
                        name = row[1]
                        print(name)
                        break
                conn.close()
            except:
                    pass
        if NoMatch:
            tolerance_tweak+=0.15
            Tries+=1
    if NoMatch:
        name = 'NA'
    return name

from urllib.request import urlretrieve
def saveImage(url):
    print("Image Method Called")
    urlretrieve(url, "C:\\Users\\manohar.k\\source\\repos\\KekaHr\\KekaHr\\MultiFaceDetector\\data\\img.jpg")
    print("Image Stored successfully")

import urllib.parse
@csrf_exempt
def processImage(request):
    if(request.method == 'POST'):
        data = request.body
        data = dict(urllib.parse.parse_qsl(data))
        url = data[b'url'].decode('UTF-8')
        saveImage(url)
        name = MatchFaceData()
        return HttpResponse(f'<h1>{name}</h1>')
    else:
        return HttpResponse("<b>A GET Request will not be processed</b>")