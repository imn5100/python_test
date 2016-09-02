# -*- coding: utf-8 -*-
def is_palindrome(n):
    n=str(n)
    length = len(n)
    i=0
    while i<=length/2:
        if n[i]!=n[length-1-i]:
            return False
        i=i+1
    return True
output = filter(is_palindrome, range(1, 5000))
print(list(output))
        