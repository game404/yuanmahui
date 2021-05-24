import time

"""二进制实现"""


def my_add(num1, num2):
    # write code here
    if not num1:
        return num2
    elif not num2:
        return num1
    while num2:
        num1, num2 = (num1 ^ num2) & 0xFFFFFFFF, (num1 & num2) << 1

    if num1 >> 31 == 0:
        return num1
    else:
        return num1 - 4294967296


start = time.time()
number = 0
for i in range(100000000):
    number = my_add(number, i)

print(number)
print(f"Elapsed time: {time.time() - start} s")
