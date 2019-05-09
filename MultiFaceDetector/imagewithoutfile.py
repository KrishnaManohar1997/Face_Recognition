import io
import urllib.request

from PIL import Image

# your avatar URL as example
url = ('https://www.gravatar.com/avatar/3341748e9b07c9854d50799e0e247fa3'
       '?s=328&d=identicon&response=PG&f=1')
content = urllib.request.urlopen(url).read()
print(type(content))
original_image = Image.open(io.BytesIO(content))
print(type(original_image))