"""Promise implementation."""
import sys

from collections import deque
import inspect
from weakref import ref, WeakMethod

from .abstract import Thenable
from .utils import reraise

__all__ = ['promise']


@Thenable.register
class promise:
    """Promise of future evaluation.

    This is a special implementation of promises in that it can
    be used both for "promise of a value" and lazy evaluation.
    The biggest upside for this is that everything in a promise can also be
    a promise, e.g. filters, callbacks and errbacks can all be promises.

    Usage examples:

    .. code-block:: python

        >>> p = promise()
        >>> p.then(promise(print, ('OK',)))  # noqa
        >>> p.on_error = promise(print, ('ERROR',))  # noqa
        >>> p(20)
        OK, 20
        >>> p.then(promise(print, ('hello',)))  # noqa
        hello, 20


        >>> p.throw(KeyError('foo'))
        ERROR, KeyError('foo')


        >>> p2 = promise()
        >>> p2.then(print)  # noqa
        >>> p2.cancel()
        >>> p(30)

    Example:
    .. code-block:: python

        from vine import promise, wrap

        class Protocol(object):

            def __init__(self):
                self.buffer = []

            def receive_message(self):
                return self.read_header().then(
                    self.read_body).then(
                        wrap(self.prepare_body))

            def read(self, size, callback=None):
                callback = callback or promise()
                tell_eventloop_to_read(size, callback)
                return callback

            def read_header(self, callback=None):
                return self.read(4, callback)

            def read_body(self, header, callback=None):
                body_size, = unpack('>L', header)
                return self.read(body_size, callback)

            def prepare_body(self, value):
                self.buffer.append(value)
    """

    if not hasattr(sys, 'pypy_version_info'):  # pragma: no cover
        __slots__ = (
            'fun', 'args', 'kwargs', 'ready', 'failed',
            'value', 'ignore_result', 'reason', '_svpending', '_lvpending',
            'on_error', 'cancelled', 'weak', '__weakref__',
        )

    def __init__(self, fun=None, args=None, kwargs=None,
                 callback=None, on_error=None, weak=False,
                 ignore_result=False):
        self.weak = weak
        self.ignore_result = ignore_result
        # 要执行的函数
        self.fun = self._get_fun_or_weakref(fun=fun, weak=weak)
        # 注意位置参数是元祖，这样才可以在call里叠加
        self.args = args or ()
        # 关键字参数是字典
        self.kwargs = kwargs or {}
        # ready，failed，cancelled 三个状态，默认都是false
        self.ready = False
        self.failed = False
        self.value = None
        self.reason = None
        # Optimization
        # Most promises will only have one callback, so we optimize for this
        # case by using a list only when there are multiple callbacks.
        #   s(calar) pending / l(ist) pending
        # 单个callback/多个callback
        self._svpending = None
        self._lvpending = None
        self.on_error = on_error
        self.cancelled = False
        # 可见callback可以通过参数传递，也可以通过then函数传递
        if callback is not None:
            self.then(callback)

        if self.fun:
            assert self.fun and callable(fun)

    @staticmethod
    def _get_fun_or_weakref(fun, weak):
        """Return the callable or a weak reference.

        Handles both bound and unbound methods.
        """
        # 是否使用弱引用
        if not weak:
            return fun
        # 区分方法和函数
        if inspect.ismethod(fun):
            return WeakMethod(fun)
        else:
            return ref(fun)

    def __repr__(self):
        return ('<{0} --> {1!r}>' if self.fun else '<{0}>').format(
            f'{type(self).__name__}@0x{id(self):x}', self.fun,
        )

    def cancel(self):
        self.cancelled = True
        try:
            if self._svpending is not None:
                self._svpending.cancel()
            if self._lvpending is not None:
                for pending in self._lvpending:
                    pending.cancel()
            if isinstance(self.on_error, Thenable):
                self.on_error.cancel()
        finally:
            self._svpending = self._lvpending = self.on_error = None

    def __call__(self, *args, **kwargs):
        retval = None
        if self.cancelled:
            return
        # 叠加参数
        final_args = self.args + args if args else self.args
        final_kwargs = dict(self.kwargs, **kwargs) if kwargs else self.kwargs
        # self.fun may be a weakref
        fun = self._fun_is_alive(self.fun)
        if fun is not None:
            try:
                if self.ignore_result:
                    fun(*final_args, **final_kwargs)
                    ca = ()
                    ck = {}
                else:
                    # 执行函数
                    retval = fun(*final_args, **final_kwargs)
                    self.value = (ca, ck) = (retval,), {}
            except Exception:
                # 异常
                return self.throw()
        else:
            self.value = (ca, ck) = final_args, final_kwargs
        # 更改ready状态
        self.ready = True
        svpending = self._svpending
        # 执行callback，把fun执行的结果往callback里传入这样形成pipeline
        if svpending is not None:
            try:
                svpending(*ca, **ck)
            finally:
                self._svpending = None
        else:
            lvpending = self._lvpending
            try:
                while lvpending:
                    # 从左开始执行
                    p = lvpending.popleft()
                    p(*ca, **ck)
            finally:
                self._lvpending = None
        return retval

    def _fun_is_alive(self, fun):
        # weak的时候直接执行一次
        return fun() if self.weak else self.fun

    def then(self, callback, on_error=None):
        # callback是普通函数，就用promise再嵌套一下
        if not isinstance(callback, Thenable):
            callback = promise(callback, on_error=on_error)
        if self.cancelled:
            callback.cancel()
            return callback
        if self.failed:
            callback.throw(self.reason)
        elif self.ready:
            args, kwargs = self.value
            callback(*args, **kwargs)
        if self._lvpending is None:
            svpending = self._svpending
            if svpending is not None:
                self._svpending, self._lvpending = None, deque([svpending])
            else:
                # 初始复制callback给_svpending
                # 就是一种递归
                self._svpending = callback
                return callback
        # 添加到右侧
        self._lvpending.append(callback)
        # 返回的是一个promise可以继续then，实现a.then(fun_x).then(fun_y).then(fun_z) 这样的链式调用
        return callback

    def throw1(self, exc=None):
        if not self.cancelled:
            exc = exc if exc is not None else sys.exc_info()[1]
            self.failed, self.reason = True, exc
            if self.on_error:
                self.on_error(*self.args + (exc,), **self.kwargs)

    def throw(self, exc=None, tb=None, propagate=True):
        if not self.cancelled:
            current_exc = sys.exc_info()[1]
            exc = exc if exc is not None else current_exc
            try:
                self.throw1(exc)
                svpending = self._svpending
                # 错误也逐个传递
                if svpending is not None:
                    try:
                        svpending.throw1(exc)
                    finally:
                        self._svpending = None
                else:
                    lvpending = self._lvpending
                    try:
                        while lvpending:
                            lvpending.popleft().throw1(exc)
                    finally:
                        self._lvpending = None
            finally:
                if self.on_error is None and propagate:
                    if tb is None and (exc is None or exc is current_exc):
                        raise
                    reraise(type(exc), exc, tb)

    @property
    def listeners(self):
        if self._lvpending:
            return self._lvpending
        return [self._svpending]
