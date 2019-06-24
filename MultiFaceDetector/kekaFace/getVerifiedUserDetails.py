from MultiFaceDetector.kekaFace.generateFaceEncoding import generateFaceEncoding
import numpy as np
from MultiFaceDetector.kekaFace.initializeCursor import initializeCursor
import face_recognition as fr
from MultiFaceDetector.kekaFace.statusCode import StatusCode
def getVerifiedUserDetails(originalImage,getEncoding = 0):
    employeeName = None
    employeeId = None
    encodingToCheck = generateFaceEncoding(originalImage)
    if(isinstance(encodingToCheck,int) and (encodingToCheck == StatusCode.NoFace.value or encodingToCheck == StatusCode.MultipleFaces.value)):
        return encodingToCheck
        """
        This Will Return 0 or 2
        If more than one face is detected, the response will be 2 indicating
        more than one face in the screen
        """
    elif(isinstance(encodingToCheck,np.ndarray)):
        try:
            cursor,conn = initializeCursor()
            cursor.execute("SELECT FaceEncoding,EmployeeName,EmployeeId from EmployeeFaceEncodings WHERE FaceRegistrationStatus = 1")
            for row in cursor.fetchall():
                existingEncoding = np.frombuffer(row[0],dtype = "float64")
                matches = fr.compare_faces([existingEncoding],encodingToCheck,tolerance = 0.48)
                if True in matches:
                    employeeName = row[1]
                    employeeId = row[2]
                    return (employeeId,employeeName)
            """
            When no user is Matched or Identified
            """
            if(getEncoding is True):
                return encodingToCheck
            else:
                return StatusCode.UnregisteredUser.value
        except Exception as e:
            print(e)
            print("ODBC Connection Error")
            return StatusCode.ServerError.value