import time
from functools import reduce
from operator import add

start = time.time()


def my_add(a, b):
    return a + b


number = reduce(add, range(100000000))

print(number)
print(f"Elapsed time: {time.time() - start} s")
