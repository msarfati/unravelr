#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

import os
from io import BytesIO
from instacommander.images import ANSIImage


img = BytesIO(open("./bin/led-hallway.jpg", 'rb').read())  # filename

get_tty_width = lambda: int(os.popen('stty size').read().split()[1])
output_size = round(get_tty_width() / 1.15)

ansi = ANSIImage(img, output_size)

print(ansi.stream)
# print("\x1b[0m\n")
