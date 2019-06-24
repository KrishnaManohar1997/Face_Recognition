import numpy as np
from MultiFaceDetector.kekaFace.faceEncodingToBlob import adaptArray,convertArray
import sqlite3
def initializeCursor():
    con = sqlite3.connect('KekaFaceRecognition.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = con.cursor()
    sqlite3.register_adapter(np.ndarray, adaptArray)
    sqlite3.register_converter("array", convertArray)
    # cursor.execute('''
    #                 CREATE TABLE IF NOT EXISTS 
    #                 EmployeeFaceEncodings (EmployeeId INTEGER PRIMARY KEY AUTOINCREMENT
    #                 ,FaceEncoding array
    #                 ,EmployeeName TEXT NOT NULL
    #                 ,FaceRegistrationStatus INTEGER
    #                 ,EmployeeImage TEXT)
    #                 ''')
    return (cursor,con)