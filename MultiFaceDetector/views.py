from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from io import BytesIO
import face_recognition
import numpy as np
import io
from urllib.request import urlopen
import mysql.connector as mysql
from mysql.connector import Error
import os
import urllib.parse
import json
import base64
dirname = os.path.dirname(__file__)
image_directory = os.path.join(dirname, 'data\\img.jpg')
def MatchFaceData(imageData):
    Saved_Encodings = []
    Saved_Names = []
    DB_NAME = "9JRQMmVx9k"
    SqlDB = mysql.connect(
        host = "remotemysql.com",
        port = "3306",
        user = "9JRQMmVx9k",
        password = "RWiVc5LET0",
        database = DB_NAME,
        use_pure = True
        )
    cursor = SqlDB.cursor()
    cursor.execute("SELECT FaceEncoding,EmployeeName from EmployeeFaceEncodings")
    for row in cursor.fetchall():
        Saved_Encodings.append(np.frombuffer(row[0],dtype = "float64"))
        Saved_Names.append(row[1])
    face_encodings = []
    face_names = []
    #stream = io.BytesIO(imageData)
    #img = Image.open(stream)
    #draw = ImageDraw.Draw(img)
    # bytedata = io.BytesIO(imageData)
    # data = Image.open(bytedata)
    # img8 = bytescale(data,np.uint8)

    #image = face_recognition.load_image_file(data)
    #data = Image.frombytes('RGBA',(240,360),imageData)
    original_image = Image.open(io.BytesIO(imageData))
    print(type(original_image))
    #image = face_recognition.load_image_file(original_image,mode='RGB')
    #image = face_recognition.load_image_file(image_directory)
    face_encodings = face_recognition.face_encodings(np.array(original_image))
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(Saved_Encodings, face_encoding,tolerance = 0.48)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = Saved_Names[first_match_index]     
        face_names.append(name)
    return face_names

@csrf_exempt
def processImage(request):
    if(request.method == 'POST'):
        data = str(request.body,'utf-8')
        data = json.loads(data)
        imageData = base64.b64decode(data['imgData'])
        #image_result = open(image_directory, 'wb')
        #image_result.write(imageData)
        name = MatchFaceData(imageData)
        return HttpResponse(f'{name}')
    else:
        return HttpResponse("<b>A GET Request will not be processed</b>")