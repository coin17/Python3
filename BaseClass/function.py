# -*- coding: utf-8 -*-
import math

#定义方法，默认参数
def enroll(name,gender,age=6,city='Beijing'):
	print('name:',name)
	print('gender:',gender)
	print('age:',age)
	print('city:',city)

#定义方法，可变参数，多个变量组成的list  
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum

#print(calc(1,2,3))

#定义方法，关键字参数 
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)

#person('Coin',11,address='Beijing',email='xiao_coin@foxmail.com')

#递归
def fact(n):
	if n == 1:
		return 1
	return n * fact(n - 1)
#print(fact(5))

def fact(n):
    return fact_iter(n, 1)

def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)

#print(fact(5))

#循环
d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
	#print(key)
	pass
for value in d.values():
	#print(value)
	pass
for key,value in d.items():
	#print(key,value)
	pass

from collections import Iterable
#print(isinstance('abc',Iterable))
#print(isinstance([1,2,3],Iterable))
#print(isinstance(123,Iterable))

for i, value in enumerate(['A', 'B', 'C']):
	#print(i,value)
	pass

for x, y in [(1, 1), (2, 4), (3, 9)]:
	#print(x, y)
	pass

#print([x * x for x in range(1,11)])

#print([x * x for x in range(1,11) if x % 2 == 0])

#print([m + n for m in 'ABC' for n in 'XYZ'])

import os
#print([d for d in os.listdir('.')])

d = {'x': 'A', 'y': 'B', 'z': 'C' }
for k,v in d.items():
	#print(k,'=',v)
	pass

#print([k + '=' + v for k, v in d.items()])	

L = ['Hello', 'World', 'IBM', 'Apple']
#print([s.lower() for s in L])

L = ['Hello', 'World', 18, 'Apple', None]
#print([s.lower() for s in L if isinstance(s,str)])

#生成器 内存限制
L = [x * x for x in range(10)]
#print(L)

g = (x * x for x in range(10))
#print(g)
for n in g:
	#print(n)
	pass

def fib(max):
	n,a,b = 0,0,1
	while n<max:
		print(b)
		a,b = b,a+b
		n = n + 1
	return 'done'

#fib(6)

def fib(max):
	n,a,b = 0,0,1
	while n<max:
		yield b
		a,b = b,a+b
		n = n + 1
	return 'done'

g = fib(6)
while True:
	try:
		x = next(g)
		#print('g',x)
	except StopIteration as e:
		#print('Generator return value:',e.value)
		break
	else:
		pass
	finally:
		pass

#杨辉三角 不太理解
L = [1]
#print(L)
#print(len(L))
L.append(0)
#print(L)
#print(len(L))
L = [L[i] + L[i-1] for i in range(len(L))]
#print(L)
#print(len(L))

def triangle(n):
    L = [1]
    while True:
        yield(L)
        L.append(0)
        L = [L[i] + L[i-1] for i in range(len(L))]
        if len(L)>10:
            break
    return "done"

#g = triangle(5)
#for i in g:
#    print(i)

#迭代器
#Iterable
from collections import Iterable
#print(isinstance([], Iterable))

#print(isinstance({}, Iterable))

#print(isinstance('abc', Iterable))

#print(isinstance((x for x in range(10)), Iterable))

#print(isinstance(100, Iterable))

#Iterator
#print(isinstance(iter([]), Iterator))

#print(isinstance(iter('abc'), Iterator))

#高阶函数
def add(x, y, f):
    return f(x) + f(y)

#print(add(-5, 6, abs))

#map
def f(x):
	return x * x

L = []
for n in range(10):
	L.append(f(n))

#print(L)

r = map(f,range(10))
print(list(r))

r = map(str,range(10))
print(list(r))

from functools import reduce
def add(x, y):
	return x + y

print(reduce(add, [1, 3, 5, 7, 9]))

from functools import reduce

def prod(L):
    return reduce(lambda x, y: x*y, L)

print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))


from functools import reduce

def fn(x, y):
    return x*10 + y

def str2float(s):
    str1, str2 = s.split('.')
    print('小数位数：',len(str2))
    return reduce(fn, map(int, str1)) + reduce(fn, map(int, str2)) / 10**len(str2)

print('str2float(\'123.456\') =', str2float('123.456'))


def normalize(name):
	return name[0].upper() + name[1:].lower()
flag = ['adam', 'LISA', 'barT']
print(list(map(normalize,flag)))

str = "  0000000this is string example....wow!!!0000000  "
print(str.strip( '0' ))
print(str.strip())

def not_empty(s):
    return s and s.strip()

print(list(filter(not_empty, ['A', '', 'B', None, 'C', '  '])))

import json
data = [{'a':"A",'b':(2,4),'c':3.0}]  #list对象
print("DATA:",repr(data))