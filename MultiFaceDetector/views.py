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
# from django.db import connection
import time
# import pyodbc
from MultiFaceDetector.FaceEncodingToBlob import adapt_array,convert_array
import sqlite3
def initializeCursor():
    con = sqlite3.connect('KekaFaceRecognition.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
    #conn = sqlite3.connect('KekaFaceRecognition.sqlite')
    cursor = con.cursor()
    # Converts np.array to TEXT when inserting
    sqlite3.register_adapter(np.ndarray, adapt_array)

    # Converts TEXT to np.array when selecting
    sqlite3.register_converter("array", convert_array)
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS 
                    EmployeeFaceEncodings ( EmployeeId INTEGER PRIMARY KEY AUTOINCREMENT
                    ,FaceEncoding array
                    ,EmployeeName TEXT NOT NULL
                    ,isFaceRegistered INTEGER)
                    ''')
    return (cursor,con)

def verifyUser(original_image):
    face_encodings = []
    EmployeeName = None
    EmployeeId = None
    encodingToCheck = generateFaceEncoding(original_image)
    if(isinstance(encodingToCheck,int) and (encodingToCheck == 0 or encodingToCheck == 2)):
        return encodingToCheck
        # This Will Return 0 or 2
        """
        If more than 1 face is detected, the response will be 2 indicating
        more than 1 face in the screen
        """
    elif(isinstance(encodingToCheck,np.ndarray)):
    # face_encodings = face_recognition.face_encodings(faceDataArray)[0]
        try:
            # cursor = connection.cursor()
            cursor,conn = initializeCursor()
            cursor.execute("SELECT FaceEncoding,EmployeeName,EmployeeId from EmployeeFaceEncodings WHERE isFaceRegistered = 1")
            print(type(face_encodings))
            for row in cursor.fetchall():
                existingEncoding = np.frombuffer(row[0],dtype = "float64")
                # matches = face_recognition.compare_faces(Saved_Encodings, face_encoding,tolerance = 0.48)
                matches = face_recognition.compare_faces([existingEncoding],encodingToCheck,tolerance = 0.48)
                """
                After User is Verified then, checking stops,
                and values are stored in EmployeeName and EmployeeId
                """
                if True in matches:
                    EmployeeName = row[1]
                    EmployeeId = row[2]
                    print(row[1],row[2])
                    return (EmployeeName,EmployeeId)
                    # Saved_Names.append(row[1])
            return -1
            """
            returns EmployeeName as None if no user is matched
            or else Name of the Employee is sent
            """
        except Exception as e:
            print(e)
            print("ODBC Connection Error")
            return 3

@csrf_exempt
def verification(request):
    if(request.method == 'POST'):
        data = str(request.body,'utf-8')
        data = json.loads(data)
        imageData = base64.b64decode(data['imgData'])
        original_image = Image.open(io.BytesIO(imageData))
        # faceDataArray = np.array(imageData)
        name = verifyUser(original_image)
        if(isinstance(name,int)):
            if(name == -1):
                return HttpResponse("Cannot Recognize user. Are you Registerd? Else try taking picture covering your full face")    
            elif(name == 0):
                return HttpResponse("No face in given picture")
            elif(name == 2):
                return HttpResponse("More than 1 User Found in Picture")
            elif(name == 3):
                return HttpResponse("An Error occured while Connecting to Server")
        elif(isinstance(name,tuple)):
            return HttpResponse(str(name[0])+','+str(name[1]))
    else:
        return HttpResponse("<b>A GET Request will not be processed</b>")

@csrf_exempt
def registration(request):
    if(request.method == 'POST'):
        # reqdata = str(request.body,'utf-8')
        # print(reqdata)
        # data = dict(urllib.parse.parse_qs(reqdata))
        # print(data)
        # imageData = data['imgData']
        # employeeId = data['eid']
        data = str(request.body,'utf-8')
        data = json.loads(data)
        imgData = data['imgData']
        imageData = base64.b64decode(imgData)
        employeeId = data['eid']
        employeeName = data['empName']
        original_image = Image.open(io.BytesIO(imageData))
        faceDataArray = np.array(original_image)
        # imgNo = data['imgId']
        userData = verifyUser(faceDataArray)
        registrationStatus = ''
        if(isinstance(userData,int)):
            if(userData == 0):
                return HttpResponse("No face in given picture")
            elif(userData == 2):
                return HttpResponse("More than 1 User Found in Picture")
            elif(userData == 1):
                return HttpResponse("An Error occured while Connecting to Server")
            elif(userData == -1):
                registrationStatus = registerUser(imgData,faceDataArray,employeeId,employeeName)
            return HttpResponse(registrationStatus)
        elif(isinstance(userData,tuple)):
            return HttpResponse('User Already Registered'+str(userData[0])+','+str(userData[1]))
    else:
        return HttpResponse(f"<h1>GET request is not accepted for API call</h1>")

def registerUser(original_image,imgData,employeeId,employeeName):
    encodingToStore = generateFaceEncoding(imgData,num_jit = 5)
    if(isinstance(encodingToStore,int) and (encodingToStore == 0 or encodingToStore ==2)):
        return encodingToStore
    elif(isinstance(encodingToStore,np.ndarray)):
        cursor,conn = initializeCursor()
        # cursor.execute("INSERT INTO EmployeeFaceEncodings(FaceEncoding,isFaceRegistered,EmployeeImage,EmployeeId) VALUES(?,?,?,?)",(encodingToStore,1,original_image,employeeId))
        try:
            cursor.execute('UPDATE EmployeeFaceEncodings SET FaceEncoding=?,isFaceRegistered=1,EmployeeImage=? WHERE EmployeeId=?',(encodingToStore,original_image,employeeId))
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
# elif(isinstance(encodingToStore,int) and encodingToStore == 2):
#     """
#     If more than 1 face is detected, the response will be 2 indicating
#     more than 1 face in the screen
#     """
#     return 2    
    return False

def generateFaceEncoding(original_image,num_jit = 1):
    """
    image: numpy array either B/W or RGB Image
    num_jit: number of jitters used while generating the face encoding
    """
    try:
        face_encodings = face_recognition.face_encodings(np.array(original_image),num_jitters=num_jit)
        if(len(face_encodings)==0):
            return 0
        elif(len(face_encodings)>1):
            return 2
        else:
            return face_encodings[0]
    except Exception as e:
        print(e)
        return 0

def showRegisteredUsers(request):
   return employeeInfo(1)

def showUnRegisteredUsers(request):
   return employeeInfo(0)

def employeeInfo(isRegistered):
    userData = []
    try:
        cursor = initializeCursor()[0]
        for user in cursor.execute("SELECT EmployeeFaceEncodings.EmployeeId,EmployeeFaceEncodings.EmployeeName,EmployeeFaceEncodings.EmployeeImage FROM EmployeeFaceEncodings WHERE EmployeeFaceEncodings.isFaceRegistered ="+str(isRegistered)).fetchall():
            employeeData = {}
            employeeData['id'] = user[0]
            employeeData['name'] = user[1].title()
            employeeData['image'] = user[2]
            userData.append(employeeData)
        return HttpResponse(userData)
    except Exception as e:
        print(e)
    return HttpResponse("Server Failed to Respond")

@csrf_exempt
def FillDBWithUsers(request):
    cursor,conn = initializeCursor()
    empNames = ['anshul','murali','kiran','rakesh','sri ram','aparna','barun','bheeshma','chandermani','debdeep','dheeraj','eeshani','farooqui','gajanan','keerthi','kireeti','kumkum','mallika','manohar','manuj','mohan','mubin','mukesh','naveed','OM','prashanth','prashanthi','praveen','Praveena','rakesh','rishab','rohan','sandeep','sandeepP','sashi','sesha','shanthi','shiva','siva','srikanth','srinivas','subhash','sumith','surerndra','suresh','trinath','venkat','vijay','vijaya lakshmi','vinay','vishnu','yeshwanth','rahul Singh','Noyal','anand','manikanth','vikram']
    try:
        with conn:
            for name in empNames:
                cursor.execute("INSERT INTO EmployeeFaceEncodings(EmployeeName,isFaceRegistered) VALUES (?,?)",(name,0))
                conn.commit()
        return HttpResponse("<H1> Sample user data is Created</h1>")
    except Exception as e:
        return HttpResponse(e)