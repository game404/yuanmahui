import sys
import ctypes
# importing weakref module
import weakref
import gc


def test_single_refcount():
    a = 'my-string'
    # 4
    print(sys.getrefcount(a))
    # 4
    print(sys.getrefcount(a))


def test_double_refcount():
    a = 'my-string-a'
    b = [a]  # Make a list with a as an element.
    print(sys.getrefcount(a))
    c = {'key': a}  # Create a dictionary with a as one of the values.
    print(sys.getrefcount(a))


def test_ref_by_id():

    # list object which is referenced by
    # my_list
    my_list = [1, 2, 3]
    b = my_list

    # finding the id of list object
    my_list_address = id(my_list)
    ret = sys.getrefcount(my_list)

    # finds reference count of my_list
    ref_count = ctypes.c_long.from_address(my_list_address).value

    # 2
    print(f"Reference count for my_list is: {ref_count}")
    # 3
    print(ret)
    del my_list
    # referenced before assignment
    # print(sys.getrefcount(my_list))


def test_weak_ref():

    # creating a class
    class GFG(list):
        pass

    # creating object of a class
    obj = GFG("Geeks")

    # creating a normal list object
    normal_list = obj
    print(f"This is a normal object: {normal_list}")
    print(sys.getrefcount(obj))
    print(ctypes.c_long.from_address(id(obj)).value)

    # this returns a weak reference to obj
    weak_list = weakref.ref(obj)
    weak_list_obj = weak_list()
    print(f"This is a object created using weak reference: {weak_list_obj}")
    print(sys.getrefcount(obj))
    print(ctypes.c_long.from_address(id(obj)).value)

    # creating a proxy of original object
    proxy_list = weakref.proxy(obj)
    print(f"This is a proxy object: {proxy_list}")
    print(sys.getrefcount(obj))
    print(ctypes.c_long.from_address(id(obj)).value)

    # printing the count of weak references
    for objects in [normal_list, weak_list_obj, proxy_list]:
        print(f"Number of weak references: {weakref.getweakrefcount(objects)}")


def test_ref_method():
    class C:
        def method(self):
            print("method called!", id(self))

    c = C()
    print(id(c))
    c.method()
    h = c.method
    h()
    del c
    gc.collect()
    h()
    # print(id(c))


def test_weakref_method():
    def handle():
        print("handle a")

    r = weakref.ref(handle)
    handle()
    r()()
    del handle
    if r() is not None:
        r()()
    # if handle:
    # handle()

    class C:
        def method(self):
            print("method called!", id(self))

    c = C()
    c.method()
    r = weakref.ref(c)
    r().method()
    r = weakref.WeakMethod(c.method)
    r()()
    del c
    # c.mehod()
    if r() is not None:
        r()()


def test_weak_proxy():
    class C:
        def method(self):
            print("method called!", id(self))

    c = C()
    c.method()
    p = weakref.proxy(c)
    p.method()


def test_weak_value_dict(cache):
    c_list = []

    class C:
        def method(self):
            return ("method called!", id(self))

    c1 = C()
    c2 = C()
    c3 = C()
    c_list.append(c1)
    c_list.append(c2)
    c_list.append(c3)
    del c1, c2, c3

    def do_cache(cache, name, target):
        cache[name] = target

    for idx, target in enumerate(c_list):
        do_cache(cache, idx, target)

    for k, v in cache.items():
        print("before", k, v.method())
    del c_list
    gc.collect()
    for x, y in cache.items():
        print("after", x, y.method())


def test_blinker():
    from blinker import signal

    def subscriber1(sender):
        print("1 Got a signal sent by %r" % sender)
        return sender+"1"

    def subscriber2(sender):
        print("2 Got a signal sent by %r" % sender)
        print(sender+"2")

    ready = signal('ready')
    print(ready)
    ready.connect(subscriber1)
    ready.connect(subscriber2)
    result = ready.send("go")
    print(result)


if __name__ == "__main__":
    # test_single_refcount()
    # test_double_refcount()
    # test_ref_by_id()
    # test_weak_ref()
    # test_weakref_method()
    # test_weak_proxy()
    # gc.set_debug(gc.DEBUG_LEAK)
    test_weak_value_dict({})
    print("==" * 10)
    test_weak_value_dict(weakref.WeakValueDictionary())
    # test_blinker()
