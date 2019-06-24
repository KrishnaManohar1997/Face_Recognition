import face_recognition as fr
import numpy as np
from MultiFaceDetector.kekaFace.statusCode import StatusCode
def generateFaceEncoding(originalImage,numJit = 1):
    """
    image: B/W or RGB ImageData
    num_jit: number of jitters used while generating the face encoding
    """
    try:
        faceEncodings = fr.face_encodings(np.array(originalImage),num_jitters=numJit)
        if(len(faceEncodings)==0):
            return StatusCode.NoFace.value
        elif(len(faceEncodings)>1):
            return StatusCode.MultipleFaces.value
        else:
            return faceEncodings[0]
    except Exception as e:
        print(e)
        return StatusCode.NoFace.value