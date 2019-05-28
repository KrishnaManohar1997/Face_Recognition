from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from io import BytesIO
import io
from urllib.request import urlopen
import os
import urllib.parse
import json
import base64
import face_recognition
import numpy as np
from django.db import connection
import time
import pyodbc
def MatchFaceData(imageData):
    face_encodings = []
    start = time.time()
    try:
        face_encodings = face_recognition.face_encodings(np.array(imageData))[0]
        timeForGeneratingEncoding = str(time.time() - start)
        if(len(face_encodings)>0):
            # Saved_Encodings = []
            # Saved_Names = []
            # connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:kekafaces.database.windows.net,1433;Database=employeefacesdata;Uid=krishnamanohar@kekafaces;Pwd={8333038187mM*};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
            cursor = connection.cursor()
            cursor.execute("SELECT FaceEncoding,EmployeeName from EmployeeFaceEncodings")
            EmployeeName = ""
            start = time.time()
            for row in cursor.fetchall():
                # Saved_Encodings.append(np.frombuffer(row[0],dtype = "float64"))
                encodingToCheck = np.frombuffer(row[0],dtype = "float64")
                matches = face_recognition.compare_faces(encodingToCheck, [face_encodings],tolerance = 0.48)
                # matches = face_recognition.compare_faces(Saved_Encodings, face_encoding,tolerance = 0.48)
                if True in matches:
                    EmployeeName+= row[1]
                    print("#############################################")
                    print(row[1])
                    break
                    # Saved_Names.append(row[1])
            timeForFindingFace = str(time.time()-start)
            EmployeeName+=' Time for Generating Encoding : '+timeForGeneratingEncoding+ ' Time For Detecting Match : '+timeForFindingFace
            return EmployeeName
        else:
            return "Error"   
    except:
        return "Error"
@csrf_exempt
def processImage(request):
    if(request.method == 'POST'):
        start = time.time()
        data = str(request.body,'utf-8')
        data = json.loads(data)
        imageData = base64.b64decode(data['imgData'])
        dirname = os.path.dirname(__file__)
        dir = os.path.join(dirname, 'data\\img.jpg')
        image_result = open(dir, 'wb')
        image_result.write(imageData)
        original_image = Image.open(io.BytesIO(imageData))
        timeForProcessingReq = str(time.time()-start)
        name = MatchFaceData(original_image)
        totalTime = str(time.time()-start)
        return HttpResponse(name+' Time for Processing Request Data : '+timeForProcessingReq+" Whole Req and Response Time : "+totalTime)
    else:
        return HttpResponse("<b>A GET Request will not be processed</b>")
# def registerUser(request):
#     return HttpResponse("<h1>Face Registration Page</h1>")
def registerUser(request,uid):
    print("The Uid is "+str(uid))
    return HttpResponse("<h1>Uid : %s </h1>",uid)