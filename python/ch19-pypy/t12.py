import time
import sys

import psutil

try:
    xrange
except NameError:  # python3
    xrange = range


def test_0():
    class Player(object):

        def __init__(self, name, age):
            self.name = name
            self.age = age

    players = []
    for i in range(10000):
        p = Player(name="p" + str(i), age=i)
        players.append(p)
    return players


def test_1():
    class Player(object):
        __slots__ = "name", "age"

        def __init__(self, name, age):
            self.name = name
            self.age = age

    players = []
    for i in range(10000):
        p = Player(name="p" + str(i), age=i)
        players.append(p)
    return players


start = time.time()

if len(sys.argv) > 1:
    mth = "test_" + sys.argv[1]
    locals()[mth]()
else:
    test_0()

p = psutil.Process()
mem = p.memory_info()
print(mem)
print("Elapsed time:  %s s" % (time.time() - start))
