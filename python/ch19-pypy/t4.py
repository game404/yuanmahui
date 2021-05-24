import time
import psutil

start = time.time()
number = 0
for i in range(100000000):
    number += i

print(number)
p = psutil.Process()
mem = p.memory_info()
print(mem)
print(f"Elapsed time: {time.time() - start} s")
