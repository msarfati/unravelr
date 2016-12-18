#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

import os
from io import BytesIO


img = BytesIO(open("./bin/led-hallway.jpg", 'rb').read())  # filename

get_tty_width = lambda: int(os.popen('stty size').read().split()[1])
width = round(get_tty_width() / 1.15)

