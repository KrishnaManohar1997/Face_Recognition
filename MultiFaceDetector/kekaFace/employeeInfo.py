from MultiFaceDetector.kekaFace.initializeCursor import initializeCursor
from django.http import JsonResponse
from MultiFaceDetector.kekaFace.statusCode import StatusCode
def employeeInfo(FaceRegistrationStatus):
    userData = []
    try:
        cursor = initializeCursor()[0]
        for user in cursor.execute("SELECT EmployeeFaceEncodings.EmployeeId,EmployeeFaceEncodings.EmployeeName,EmployeeFaceEncodings.EmployeeImage FROM EmployeeFaceEncodings WHERE EmployeeFaceEncodings.FaceRegistrationStatus ="+str(FaceRegistrationStatus)).fetchall():
            employeeData = {}
            employeeData["id"] = user[0]
            employeeData["name"] = user[1].title()
            employeeData["image"] = user[2]
            userData.append(employeeData)
        return JsonResponse(userData,safe=False)
    except Exception as e:
        print(e)
    return JsonResponse({'status':StatusCode.ServerError.value})#'message':'Server Error Occured, Try again'})