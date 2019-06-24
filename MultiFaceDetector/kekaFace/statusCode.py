from enum import Enum
"""
    -1 User not registered, so registration will be done (Managed Internally),Else Not registered Message should be shown
    0 No face found in the picture
    1 Registration Sucessful
    2 More than 1 face found
    3 Server Error
    4 User already registered, data of the user(name and Id) will be sent
    6 Error With Request Data and Header
    7 User face registration failed
"""
class StatusCode(Enum):
    UnregisteredUser = -1
    NoFace = 0
    FaceRegistrationSuccessful = 1
    MultipleFaces = 2
    ServerError = 3
    AlreadyRegisteredUser = 4
    RequestHeaderError = 5
    FaceRegistrationUnsuccessful = 6
    FaceVerificationSuccessful = 7