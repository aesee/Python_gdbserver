# -- coding: cp1251 --
#! /usr/bin/python3

# very useful
# taked code from https://stackoverflow.com/questions/1592158/convert-hex-to-float

from ctypes import *


# convert hex to float
def hexToFloat(s):
    i = int(s, 16)                   # convert from hex to a Python int
    cp = pointer(c_int(i))           # make this into a c integer
    fp = cast(cp, POINTER(c_float))  # cast the int pointer to a float pointer
    return fp.contents.value         # dereference the pointer, get the float

if __name__ == '__main__':
    print(hexToFloat("41200000"))  # returns 1.88999996185302734375E1