import subprocess
from tempfile import NamedTemporaryFile
import os

img = open('./bin/led-hallway.jpg', 'rb')

tmp = NamedTemporaryFile()
tmp.write(img.read())

print(os.popen('img2txt ' + tmp.name).read())


# app = subprocess.Popen(['img2txt', tmp.name])

# img = BytesIO(open("./bin/led-hallway.jpg", 'rb').read())  # filename
# img2txt = subprocess.Popen(['img2txt'], stdin=subprocess.PIPE)

# ansi = img2txt.communicate(input=img.getvalue())

