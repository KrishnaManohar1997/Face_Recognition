from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from io import BytesIO
import io
from urllib.request import urlopen
import urllib.parse
import json
import base64
import face_recognition
import numpy as np
import time
from MultiFaceDetector.FaceEncodingToBlob import adapt_array,convert_array
import sqlite3
def initializeCursor():
    con = sqlite3.connect('KekaFaceRecognition.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = con.cursor()
    sqlite3.register_adapter(np.ndarray, adapt_array)
    sqlite3.register_converter("array", convert_array)
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS 
                    EmployeeFaceEncodings (EmployeeId INTEGER PRIMARY KEY AUTOINCREMENT
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
        """
        This Will Return 0 or 2
        If more than one face is detected, the response will be 2 indicating
        more than one face in the screen
        """
    elif(isinstance(encodingToCheck,np.ndarray)):
        try:
            cursor,conn = initializeCursor()
            cursor.execute("SELECT FaceEncoding,EmployeeName,EmployeeId from EmployeeFaceEncodings WHERE isFaceRegistered = 1")
            for row in cursor.fetchall():
                existingEncoding = np.frombuffer(row[0],dtype = "float64")
                matches = face_recognition.compare_faces([existingEncoding],encodingToCheck,tolerance = 0.48)
                if True in matches:
                    EmployeeName = row[1]
                    EmployeeId = row[2]
                    return (EmployeeName,EmployeeId)
            """
            When no user is Matched or Identified
            """
            return -1
        except Exception as e:
            print(e)
            print("ODBC Connection Error")
            return 3

@csrf_exempt
def verification(request):
    if(request.method == 'POST'):
        original_image = parseRequest(request.body,0)
        if(original_image is not None):
            name = verifyUser(original_image)
            if(isinstance(name,int)):
                return JsonResponse({'status':name,'message':'Error Occured'})
            elif(isinstance(name,tuple)):
                return JsonResponse({'status':1,'name':name[0],'id':name[1]})
        else:
            return JsonResponse({'status':6,'message':'Error With Request Data and Header'})
    else:
        return JsonResponse({'status':5,'message':'Get response is not accepted'})

@csrf_exempt
def registration(request):
    if(request.method == 'POST'):
        data = parseRequest(request.body,1)
        if(data is not None):
            employeeId,employeeName,base64ImageData,original_image = data
            userData = verifyUser(original_image)
            if(isinstance(userData,int)):
                if(userData == -1):
                    registrationStatus = registerUser(base64ImageData,original_image,employeeId,employeeName)
                    if(registrationStatus is True):
                        return JsonResponse({'status':1,'message':'User Registration is Successfull'})
                    else:
                        return JsonResponse({'status':7,'message':'Unsuccessfull while Registering'})
                else:
                    """
                    returns 0,2,3 or 4
                    """
                    return JsonResponse({'status':userData})
            elif(isinstance(userData,tuple)):
                return JsonResponse({'status':4,'name':userData[0],'id':userData[1]})
        else:
            return JsonResponse({'status':6,'message':'Error With Request Data and Header'})
    else:
        return JsonResponse({'status':5,'message':'Get response is not accepted'})

def registerUser(base64ImageData,original_image,employeeId,employeeName):
    encodingToStore = generateFaceEncoding(original_image,num_jit = 5)
    if(isinstance(encodingToStore,int) and (encodingToStore == 0 or encodingToStore ==2)):
        """
        If more than one face is detected, the response will be 2 indicating
        more than 1 face in the screen
        """  
        return encodingToStore
    elif(isinstance(encodingToStore,np.ndarray)):
        cursor,conn = initializeCursor()
        try:
            cursor.execute('UPDATE EmployeeFaceEncodings SET FaceEncoding=?,isFaceRegistered=1,EmployeeImage=? WHERE EmployeeId=?',(encodingToStore,base64ImageData,employeeId))
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    return False

def generateFaceEncoding(original_image,num_jit = 1):
    """
    image: B/W or RGB ImageData
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
            employeeData["id"] = user[0]
            employeeData["name"] = user[1].title()
            employeeData["image"] = user[2]
            userData.append(employeeData)
        return JsonResponse(userData,safe=False)
    except Exception as e:
        print(e)
    return JsonResponse({'status':3,'message':'Server Error Occured, Try again'})

def parseRequest(requestBody,registration = 1):
    try:
        data = str(requestBody,'utf-8')
        data = json.loads(data)
        base64ImageData = data['image']
        imageData = base64.b64decode(base64ImageData)
        original_image = Image.open(io.BytesIO(imageData))
        if(registration is 1):
            employeeId = data['id']
            employeeName = data['name']
            return (employeeId,employeeName,base64ImageData,original_image)
        elif registration is 0:
            return original_image
    except:
        return None

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
"""
    -1 User not registered, so registration will be done (Managed Internally)
    0 No face found in the picture
    1 Registration Sucessfull
    2 More than 1 face found
    3 Server Error
    4 User already registered, data of the user(name and Id) will be sent
    5 Get response is not accepted
    6 Error With Request Data and Header
    7 User face registration failed
"""