# -*- coding: utf-8 -*-
# 思维：下一组为上一组从b[0]+b[1]到b[len-2]+b[len-1]的集合前后各添加[1]
def triangles(num):
    b = [1]
    n = 1
    a = []
    while n < num:
        yield b
        for i in range(0, len(b) - 1) :
            a.append(b[i] + b[i + 1])
        b = [1] + a + [1]
        a = []
        n = n + 1
num = input("Please input number:")
num = int(num);
for n in triangles(num):
    print n
                    
        
        
        
        
