import random
from functools import cmp_to_key

"""
比较的时候传入参数为key，key一定是可以相互比较的。  
一个类是可比较，等价于这个类可以映射为可比较的类。而key就是这样一个函数，它把原始对象转化成一个可比较的对象
"""


class Man:
    def __init__(self):
        self.a = random.randint(0, 10)
        self.b = random.randint(0, 10)

    def __repr__(self):
        return f"{self.a},{self.b}"


a = [Man() for _ in range(10)]


def cmp(x: Man, y: Man):
    if x.a == y.a:
        return x.b - y.b
    return x.a - y.a


a.sort(key=cmp_to_key(cmp))
print(a)
b = sorted(a, key=cmp_to_key(cmp))
print(b)
