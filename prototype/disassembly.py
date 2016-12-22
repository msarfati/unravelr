#!/usr/bin/env python
import dis

# Disassemble an ordinary function called inside the code


def my_func():
    x = 33
    return 1 * 4 * x

dis.dis(my_func)

print("-" * 15)
print("-" * 15)

# Disassemble a function imported from elsewhere (say, user input field) and compiled
# https://stackoverflow.com/questions/15432499/python-how-to-get-the-source-from-a-code-object
from io import StringIO

user_input = \
"""\
x = 4
abs(-45353) * 3.14
1 + 3 * 4
"""

cio = StringIO(user_input)
# print(type(cio.getvalue()))
Binary = compile(cio.getvalue(), "<string>", "exec")
dis.dis(Binary)

result = dis.dis(Binary)
import ipdb; ipdb.set_trace()

# Future plans: support disassembling classes, modules and functions

user_input = \
"""
def myfunc2():
    x = 4 * 4
    return x / 2

def myfunc3():
    [i**2 for i in range(5)]
"""

cio = StringIO(user_input)
Binary = compile(cio.getvalue(), "<string>", "exec")

for i in range(len(Binary.co_names)):
    Binary_nest = compile(Binary.co_names[i], "<string>", "exec")
    dis.dis(Binary_nest)
