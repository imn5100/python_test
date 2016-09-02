# -*- coding: utf-8 -*-
import math
def  my_abs(x):
    if not isinstance(x, (int,float)):
        raise  TypeError("bad operand type")
    if x>0:
        return x
    else:
        return -x
def  qua(a,b,c):
    s = b**2-4*a*c
    if s<0:
        return None
    if s==0:
        return (-b+math.sqrt(b**2-4*a*c))/2*a
    if s>0:
        return (-b+math.sqrt(b**2-4*a*c))/2*a,(-b-math.sqrt(b**2-4*a*c))/2*a
        