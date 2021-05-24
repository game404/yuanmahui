import pydoc
import sys
import traceback
from inspect import signature
from xmlrpc.client import ServerProxy
from xmlrpc.server import DocXMLRPCServer


def simple_server():
    def is_even(n):
        """
        偶数判断
        """
        return n % 2 == 0

    server = DocXMLRPCServer(("localhost", 8000))
    server.register_function(pow)
    server.register_function(lambda x, y: x + y, 'add')
    server.register_function(is_even, "is_even")
    server.register_introspection_functions()
    server.serve_forever()


def simple_client():
    server = ServerProxy("http://localhost:8000")
    print(server.system.listMethods())
    print(server.system.methodSignature("add"))
    print(server.system.methodHelp("is_even"))


class Person:

    def __init__(self, name):
        self.name = name
        self.age = 0

    def incr(self, age):
        """
        长一岁
        :type age: int
        :rtype: int
        :return 年龄+1
        """
        self.age = age
        return self.age


def test_pydoc():
    p = Person("game404")
    doc = pydoc.getdoc(p.incr)
    print(doc)
    argspec = signature(p.incr)
    print(argspec)


def test_exec():
    def some(x, y):
        z = x / y
        return z

    try:
        some(1, 0)
    except:
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(exc_type, exc_value)
        print(repr(traceback.extract_tb(exc_tb)))
        print(traceback.format_exc())

a

def test_auto_unboxing():
    def some(a, b, c=2):
        print(a, b, c)

    def f(params):
        some(*params)

    def f2(*argv):
        some(*argv)

    f((0, 1))
    f((1, 2, 3))
    f({"a": 4, "b": 5, "c": 6})
    f2(*(1, 2, 3))
    f2(1, 2, 3)


if __name__ == '__main__':
    args = sys.argv[1:]
    if args:
        simple_client()
    else:
        simple_server()
