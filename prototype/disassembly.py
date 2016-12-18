#!/usr/bin/env python
import dis
from io import StringIO

# Disassemble an ordinary function called inside the code


def my_func():
    return 1

dis.dis(my_func)

print("-" * 15)
print("-" * 15)

# Disassemble a function imported from elsewhere (say, user input field) and compiled
user_input = \
"""\
def my_func2():
    return 1 \
"""

cio = StringIO(user_input)
Binary = compile(cio.getvalue(), "<string>", "exec")
dis.dis(Binary)
