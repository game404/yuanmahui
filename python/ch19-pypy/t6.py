import os
import time
from cffi import FFI
# gcc -O3 -Wall -fpic -shared t.c -o gsum.so

def test():
    ffi = FFI()
    ffi.cdef("size_t strlen(const char*);")
    clib = ffi.dlopen(None)
    length = clib.strlen(b"String to be evaluated.")
    print("{}".format(length))

def test1():
    start = time.time()
    _C_FUNCTION = """
    long long gaussianSum();
    """
    p = os.path.abspath(__file__)
    p = os.path.dirname(p)
    _ffi = FFI()
    _ffi.cdef(_C_FUNCTION)
    so_name = "/gsum.so"
    _lib = _ffi.dlopen(p + so_name)
    number = _lib.gaussianSum()
    print(number)
    print(f"Elapsed time: {time.time() - start} s")

if __name__ == '__main__':
    test1()