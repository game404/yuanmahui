"""Abstract classes."""
import abc
from collections.abc import Callable

__all__ = ['Thenable']


class Thenable(Callable, metaclass=abc.ABCMeta):  # pragma: no cover
    """Object that supports ``.then()``."""
    """支持then方法的抽象基类，需要实现then，throw和cancel方法"""

    __slots__ = ()

    @abc.abstractmethod
    def then(self, on_success, on_error=None):
        """成功和失败的2个回调"""
        raise NotImplementedError()

    @abc.abstractmethod
    def throw(self, exc=None, tb=None, propagate=True):
        raise NotImplementedError()

    @abc.abstractmethod
    def cancel(self):
        raise NotImplementedError()

    @classmethod
    def __subclasshook__(cls, C):
        # 也由ABCMeta提供
        if cls is Thenable:
            if any('then' in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented

    @classmethod
    def register(cls, other):
        # overide to return other so `register` can be used as a decorator
        # 这个register方法是由ABCMeta提供，其实现类使用装饰器方式
        # https://docs.python.org/zh-cn/3/library/abc.html
        type(cls).register(cls, other)
        return other


@Thenable.register
class ThenableProxy:
    """Proxy to object that supports ``.then()``."""
    """代理类，实质上实现了Thenable, 具体功能由p(promise实现)， 并额外实现了throw1，不带traceback的实现"""

    def _set_promise_target(self, p):
        self._p = p

    def then(self, on_success, on_error=None):
        return self._p.then(on_success, on_error)

    def cancel(self):
        return self._p.cancel()

    def throw1(self, exc=None):
        return self._p.throw1(exc)

    def throw(self, exc=None, tb=None, propagate=True):
        return self._p.throw(exc, tb=tb, propagate=propagate)

    @property
    def cancelled(self):
        return self._p.cancelled

    @property
    def ready(self):
        return self._p.ready

    @property
    def failed(self):
        return self._p.failed
