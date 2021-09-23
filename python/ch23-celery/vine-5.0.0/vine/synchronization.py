"""Synchronization primitives."""
from .abstract import Thenable
from .promises import promise

__all__ = ['barrier']


class barrier:
    """Barrier.

    Synchronization primitive to call a callback after a list
    of promises have been fulfilled.

    同样实现Thenable接口，可以批量处理promise，注意是同步串行

    Example:

    .. code-block:: python

        # Request supports the .then() method.
        p1 = http.Request('http://a')
        p2 = http.Request('http://b')
        p3 = http.Request('http://c')
        requests = [p1, p2, p3]

        def all_done():
            pass  # all requests complete

        b = barrier(requests).then(all_done)

        # oops, we forgot we want another request
        b.add(http.Request('http://d'))

    Note that you cannot add new promises to a barrier after
    the barrier is fulfilled.
    """

    def __init__(self, promises=None, args=None, kwargs=None,
                 callback=None, size=None):
        # Promise的实现
        self.p = promise()
        self.args = args or ()
        self.kwargs = kwargs or {}
        self._value = 0
        self.size = size or 0
        if not self.size and promises:
            # iter(l) calls len(l) so generator wrappers
            # can only return NotImplemented in the case the
            # generator is not fully consumed yet.
            plen = promises.__len__()
            if plen is not NotImplemented:
                self.size = plen
        self.ready = self.failed = False
        self.reason = None
        self.cancelled = False
        self.finalized = False
        # 列表推导式
        [self.add_noincr(p) for p in promises or []]
        self.finalized = bool(promises or self.size)
        if callback:
            self.then(callback)

    def __call__(self, *args, **kwargs):
        # 判断是否已经执行完成：ready和cancelled
        if not self.ready and not self.cancelled:
            self._value += 1
            if self.finalized and self._value >= self.size:
                self.ready = True
                self.p(*self.args, **self.kwargs)

    def finalize(self):
        if not self.finalized and self._value >= self.size:
            self.p(*self.args, **self.kwargs)
        self.finalized = True

    def cancel(self):
        self.cancelled = True
        self.p.cancel()

    def add_noincr(self, p):
        if not self.cancelled:
            # 已经完成了就不能够再添加了
            if self.ready:
                raise ValueError('Cannot add promise to full barrier')
            # 其实就是then().then().then() 添加到自己之前，自己主要执行最开始定义的callback
            p.then(self)

    def add(self, p):
        if not self.cancelled:
            self.add_noincr(p)
            self.size += 1

    def then(self, callback, errback=None):
        self.p.then(callback, errback)

    def throw(self, *args, **kwargs):
        if not self.cancelled:
            self.p.throw(*args, **kwargs)
    throw1 = throw

# 统一风格成使用类装饰器多好
Thenable.register(barrier)  # noqa: E305
