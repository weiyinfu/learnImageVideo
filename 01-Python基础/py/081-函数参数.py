def haha(x, y, one=1, two=2):
    return x + y


import inspect

print(inspect.getfullargspec(haha))
print(inspect.arg)
