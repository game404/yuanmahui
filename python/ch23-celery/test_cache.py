from functools import lru_cache

cache = {}


def fib_v1(n):
    if n in cache:
        return cache[n]
    if n <= 1:
        result = n
    else:
        result = fib(n - 1) + fib(n - 2)
    cache[n] = result
    return result


def cache_decorator(fun):
    _cache = {}

    def wrapper(*args, **kwargs):
        if args in _cache:
            return _cache[args]
        else:
            ret = fun(*args, **kwargs)
            _cache[args] = ret
            return ret

    return wrapper


# @cache_decorator
@lru_cache()
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


def test1():
    print(fib(5))
    print(fib_v1(5))


if __name__ == '__main__':
    test1()
