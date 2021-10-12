import sys
import vine
from vine.abstract import Thenable


class CanThen:

    def then(self, x, y):
        pass


class CannotThen:
    pass


def main():
    print(sys.version_info)
    print(vine.version_info)
    print("CanThen is Thenable", isinstance(CanThen(), Thenable))


if __name__ == '__main__':
    main()
