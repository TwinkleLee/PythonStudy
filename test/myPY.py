from collections.abc import Iterable
from collections.abc import Iterator
import t1

# num1 = 100

# obj = {'args1': 1, 'args2': 2}


# def f1(a, b, c=0, *args, **kw):
#     print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)


# f1('aa', 'bb', 'cc', 'dd', **obj)

# L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
# S = "hello world"
# print(obj.items())
# print(obj.values())

# for k, item in obj.items():
#     print(k, item)
# for i, value in enumerate(L[1:]):
#     print(i, value)

# print(isinstance('abc', Iterable))  # str是否可迭代

# for x, y in [(1, 1), (2, 4), (3, 9)]:
#     print(x, y)

# print(type(10))

# myIter = iter('abc')
# myList = list(myIter)
# print(myList)
# print(type(myList))
# print(isinstance(myList, Iterator))
# print(isinstance(myList, Iterable))
# print(isinstance(myList, list))


# def log(func):
#     def wrapper(*args, **kw):
#         print("call1",func.__name__)
#         func(*args, **kw)
#         # return func(*args, **kw)
#         print("call2",func.__name__)

#     return wrapper

# @log
# def now():
#     print('2015-3-25')


# now()
'hello world'
print("__doc__",__doc__)
print("t1.__doc__",t1.__doc__)
print("t1.author",t1.author)
print("mian__name__",__name__)


def fun():
  """hello I am fun"""
  # pass
print(fun.__doc__)