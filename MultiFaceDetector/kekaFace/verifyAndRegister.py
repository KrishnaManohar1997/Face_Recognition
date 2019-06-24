from MultiFaceDetector.kekaFace.parseRequest import parseRequest
from MultiFaceDetector.kekaFace.getVerifiedUserDetails import getVerifiedUserDetails
from MultiFaceDetector.kekaFace.registerUser import registerUser
from MultiFaceDetector.kekaFace.statusCode import StatusCode
from django.http import JsonResponse
import numpy as np
def verifyAndRegister(request):
    data = parseRequest(request.body,1)
    if(data is not None):
        employeeId,employeeName,base64ImageData,originalImage = data
        userData = getVerifiedUserDetails(originalImage,True)
        if(isinstance(userData,np.ndarray)):
            registrationStatus = registerUser(employeeId,employeeName,base64ImageData,originalImage,userData)
            if(registrationStatus is True):
                return JsonResponse({'status':StatusCode.FaceRegistrationSuccessful.value,'message':'User Registration is Successfull'})
            else:
                return JsonResponse({'status':StatusCode.FaceRegistrationUnsuccessful.value,'message':'Unsuccessfull while Registering'})
        elif(isinstance(userData,int)):            
            """
            returns 0,2,3 or 4
            """
            return JsonResponse({'status':userData})
        elif(isinstance(userData,tuple)):
            return JsonResponse({'status':StatusCode.AlreadyRegisteredUser.value,'id':userData[0],'name':userData[1]})
    else:
        return JsonResponse({'status':StatusCode.RequestHeaderError.value,'message':'Error With Request Data and Header'})