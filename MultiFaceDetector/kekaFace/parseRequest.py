import json
import base64
from PIL import Image
import io
def parseRequest(requestBody,registration = 1):
    try:
        data = str(requestBody,'utf-8')
        data = json.loads(data)
        base64ImageData = data['image']
        imageData = base64.b64decode(base64ImageData)
        originalImage = Image.open(io.BytesIO(imageData))
        if(registration is 1):
            employeeId = data['id']
            employeeName = data['name']
            return (employeeId,employeeName,base64ImageData,originalImage)
        elif registration is 0:
            return originalImage
    except:
        return None