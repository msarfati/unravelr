#!/usr/bin/env python
import dis

# Disassemble an ordinary function called inside the code


def my_func():
    return 1

dis.dis(my_func)

print("-" * 15)
print("-" * 15)

# Disassemble a function imported from elsewhere (say, user input field) and compiled
# https://stackoverflow.com/questions/15432499/python-how-to-get-the-source-from-a-code-object
from io import StringIO

user_input = \
"""\
def my_func2():
    return 1 \
"""

cio = StringIO(user_input)
Binary = compile(cio.getvalue(), "<string>", "exec")
dis.dis(Binary)
