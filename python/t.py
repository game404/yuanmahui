class Person(object):

    def hello(self):
        print("hello", self.name)


if __name__ == '__main__':
    p = Person()
    p.name = "aaa"
    print(p.name)
