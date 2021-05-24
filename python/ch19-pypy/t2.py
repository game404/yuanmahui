import time

start = time.time()
number = 0
i = 0
while 1:
    number += i
    i += 1
    if i >= 100000000:
        break

print(number)
print(f"Elapsed time: {time.time() - start} s")
