# -*- coding: utf-8 -*-
from functools import reduce
def normalize(name):
    return name[0].upper() + name[1:len(name)].lower()
def prod(n, m):
    return n * m
def my_sum(n, m):
    return n + m

def reverse (s):  
    return reduce(lambda x, y:y + x, s)  
def str2float(st):
    def char2float(s):
        return  {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
    def fn1(x, y):
        return x * 10 + y
    def fn2(x, y):
        return x / 10.0 + y
    nums = st.split('.');
    if len(nums) == 1:
        return reduce(fn1, map(char2float, st));
    if len(nums) == 2:
        return  reduce(fn1, map(char2float, nums[0])) + reduce(fn2, map(char2float, str((nums[1])[::-1]))) / 10;
    
# L1 = ['adam', 'LISA', 'barT']
# L2 = list(map(normalize, L1))
# print(L2)
# print(reduce(prod, [3, 5, 7, 9]))
# print(reduce(my_sum, [3, 5, 7, 9]))
print (str2float("31.134121"))


L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
def by_name(L):
    def get_name(L1):
        return L1[0]
    return sorted(L, key=get_name)
print(by_name(L))
print(L)
