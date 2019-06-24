from MultiFaceDetector.kekaFace.parseRequest import parseRequest
from MultiFaceDetector.kekaFace.getVerifiedUserDetails import getVerifiedUserDetails
from django.http import JsonResponse
from MultiFaceDetector.kekaFace.statusCode import StatusCode
def verifyUser(request):
    originalImage = parseRequest(request.body,0)
    if(originalImage is not None):
        userData = getVerifiedUserDetails(originalImage)
        if(isinstance(userData,int)):
            return JsonResponse({'status':userData})
        elif(isinstance(userData,tuple)):
            return JsonResponse({'status':StatusCode.FaceVerificationSuccessful.value,'id':userData[0],'name':userData[1]})
    else:
        return JsonResponse({'status':StatusCode.RequestHeaderError.value,'message':'Error With Request Data and Header'})