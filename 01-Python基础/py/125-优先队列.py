import random
from functools import cmp_to_key
from queue import PriorityQueue


class Man:
    def __init__(self):
        self.a = random.randint(0, 10)
        self.b = random.randint(0, 10)

    def __repr__(self):
        return f"{self.a},{self.b}"


def get_q(cmp):
    q = PriorityQueue()
    C = cmp_to_key(cmp)

    old_put = q.put
    old_get = q.get

    def put(x):
        old_put(C(x))

    def get():
        return old_get().obj

    q.put = put
    q.get = get
    return q


def cmp1(x: Man, y: Man):
    return -1 if (x.a, x.b) < (y.a, y.b) else 1


def cmp2(x: Man, y: Man):
    return -1 if (x.a, x.b) > (y.a, y.b) else 1


q1 = get_q(cmp1)
q2 = get_q(cmp2)
a = [Man() for _ in range(10)]
for i in a:
    q1.put(i)
    q2.put(i)


def q2a(q: PriorityQueue):
    a = []
    while not q.empty():
        a.append(q.get())
    return a


print(a)
print(q2a(q1))
print(q2a(q2))
