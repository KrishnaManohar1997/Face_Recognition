from django.views.decorators.http import require_http_methods
from MultiFaceDetector.kekaFace.employeeInfo import employeeInfo
from MultiFaceDetector.kekaFace.verifyUser import verifyUser
from MultiFaceDetector.kekaFace.verifyAndRegister import verifyAndRegister

@require_http_methods(["POST"])
def verification(request):
    return verifyUser(request)

@require_http_methods(["POST"])
def registration(request):
    return verifyAndRegister(request)

@require_http_methods(["GET"])
def showRegisteredUsers(request):
   return employeeInfo(1)

@require_http_methods(["GET"])
def showUnRegisteredUsers(request):
   return employeeInfo(0)

# from django.http import HttpResponse
# from django.http import HttpRequest
# @csrf_exempt
# def FillDBWithUsers(request):
#     cursor,conn = initializeCursor()
#     empNames = ['anshul','murali','kiran','rakesh','sri ram','aparna','barun','bheeshma','chandermani','debdeep','dheeraj','eeshani','farooqui','gajanan','keerthi','kireeti','kumkum','mallika','manohar','manuj','mohan','mubin','mukesh','naveed','OM','prashanth','prashanthi','praveen','Praveena','rakesh','rishab','rohan','sandeep','sandeepP','sashi','sesha','shanthi','shiva','siva','srikanth','srinivas','subhash','sumith','surerndra','suresh','trinath','venkat','vijay','vijaya lakshmi','vinay','vishnu','yeshwanth','rahul Singh','Noyal','anand','manikanth','vikram']
#     try:
#         with conn:
#             for name in empNames:
#                 cursor.execute("INSERT INTO EmployeeFaceEncodings(EmployeeName,isFaceRegistered) VALUES (?,?)",(name,0))
#                 conn.commit()
#         return HttpResponse("<H1> Sample user data is Created</h1>")
#     except Exception as e:
#         return HttpResponse(e)