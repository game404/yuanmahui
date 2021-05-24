import time

start = time.time()


def gaussian_sum(total: int) -> int:
    if total & 1 == 0:
        return (1 + total) * int(total / 2)
    else:
        return total * int((total - 1) / 2) + total


# 4999999950000000
number = gaussian_sum(100000000 - 1)

print(number)

print(f"Elapsed time: {time.time() - start} s")
