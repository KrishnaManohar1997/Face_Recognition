from MultiFaceDetector.kekaFace.generateFaceEncoding import generateFaceEncoding
from MultiFaceDetector.kekaFace.initializeCursor import initializeCursor
import numpy as np
def registerUser(employeeId,employeeName,base64ImageData,originalImage,encodingToStore):
    cursor,conn = initializeCursor()
    try:
        cursor.execute('UPDATE EmployeeFaceEncodings SET FaceEncoding=?,FaceRegistrationStatus=1,EmployeeImage=? WHERE EmployeeId=?',(encodingToStore,base64ImageData,employeeId))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False