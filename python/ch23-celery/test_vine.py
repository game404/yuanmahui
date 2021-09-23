from vine import promise


def main():
    p = promise()
    p.then(promise(print, ('OK',)))  # noqa
    p.on_error = promise(print, ('ERROR',))  # noqa
    p(20)


if __name__ == '__main__':
    main()
