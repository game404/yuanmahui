import time

start = time.time()
number: int = 0
for i in range(100000000):
    number += i

print(number)
print(f"Elapsed time: {time.time() - start} s")
