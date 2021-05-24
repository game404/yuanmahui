import time
import sys

try:
    xrange
except NameError:  # python3
    xrange = range


def test_0():
    number = 0
    for i in range(100000000):
        if i % 2 == 0:
            number += i
    return number


def test_1():
    number = 0

    for i in xrange(0, 100000000, 2):
        number += i
    return number


def test_2():
    number = 0
    for i in range(100000000):
        if i & 1 == 0:
            number += i
    return number


start = time.time()

if len(sys.argv) > 1:
    mth = "test_" + sys.argv[1]
    print(locals()[mth]())
else:
    print(test_0())

print("Elapsed time:  %s s" % (time.time() - start))
