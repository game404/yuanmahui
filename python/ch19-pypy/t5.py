import time
import psutil

start = time.time()


def test():
    number = 0
    for i in range(100000000):
        number += i


for x in range(10):
    t1 = time.time()
    test()
    print(f"Elapsed time: {time.time() - t1} s")

p = psutil.Process()
mem = p.memory_info()
print(mem)
print(f"total Elapsed time: {time.time() - start} s")
