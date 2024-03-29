"""Generic resource pool implementation."""

from collections import deque
import os
from queue import Empty, LifoQueue as _LifoQueue

from . import exceptions
from .utils.compat import register_after_fork
from .utils.functional import lazy


def _after_fork_cleanup_resource(resource):
    try:
        resource.force_close_all()
    except Exception:
        pass


class LifoQueue(_LifoQueue):
    """Last in first out version of Queue."""
    """后进先出的队列(栈)"""

    def _init(self, maxsize):
        # 使用双端队列取代默认的列表
        self.queue = deque()


class Resource:
    """Pool of resources."""
    """资源池"""

    LimitExceeded = exceptions.LimitExceeded

    close_after_fork = False

    def __init__(self, limit=None, preload=None, close_after_fork=None):
        self._limit = limit
        self.preload = preload or 0
        self._closed = False
        self.close_after_fork = (
            close_after_fork
            if close_after_fork is not None else self.close_after_fork
        )

        self._resource = LifoQueue()
        self._dirty = set()
        if self.close_after_fork and register_after_fork is not None:
            register_after_fork(self, _after_fork_cleanup_resource)
        self.setup()

    def setup(self):
        raise NotImplementedError('subclass responsibility')

    def _add_when_empty(self):
        if self.limit and len(self._dirty) >= self.limit:
            raise self.LimitExceeded(self.limit)
        # All taken, put new on the queue and
        # try get again, this way the first in line
        # will get the resource.
        # TODO self.new 未名
        self._resource.put_nowait(self.new())

    def acquire(self, block=False, timeout=None):
        """Acquire resource.

        Arguments:
            block (bool): If the limit is exceeded,
                then block until there is an available item.
            timeout (float): Timeout to wait
                if ``block`` is true.  Default is :const:`None` (forever).

        Raises:
            LimitExceeded: if block is false and the limit has been exceeded.
        """
        """申请资源"""
        if self._closed:
            raise RuntimeError('Acquire on closed pool')
        if self.limit:
            # 循环直到获取到一个资源
            while 1:
                try:
                    R = self._resource.get(block=block, timeout=timeout)
                except Empty:
                    # 池为空的时候增加一个
                    self._add_when_empty()
                else:
                    try:
                        R = self.prepare(R)
                    except BaseException:
                        if isinstance(R, lazy):
                            # not evaluated yet, just put it back
                            self._resource.put_nowait(R)
                        else:
                            # evaluted so must try to release/close first.
                            self.release(R)
                        raise
                    # 已经使用的资源标记为脏
                    self._dirty.add(R)
                    break
        else:
            # 池无上限则直接获取
            R = self.prepare(self.new())

        def release():
            """Release resource so it can be used by another thread.

            Warnings:
                The caller is responsible for discarding the object,
                and to never use the resource again.  A new resource must
                be acquired if so needed.
            """
            self.release(R)
        # 增加释放方法
        R.release = release

        return R

    def prepare(self, resource):
        # 父类是直接返回，子类可以覆盖，进行更多的资源准备工作
        return resource

    def close_resource(self, resource):
        # TODO close方法来自？
        resource.close()

    def release_resource(self, resource):
        pass

    def replace(self, resource):
        """Replace existing resource with a new instance.

        This can be used in case of defective resources.
        """
        """释放资源"""
        if self.limit:
            self._dirty.discard(resource)
        self.close_resource(resource)

    def release(self, resource):
        if self.limit:
            # 移除脏标记
            self._dirty.discard(resource)
            self._resource.put_nowait(resource)
            self.release_resource(resource)
        else:
            self.close_resource(resource)

    def collect_resource(self, resource):
        pass

    def force_close_all(self):
        """Close and remove all resources in the pool (also those in use).

        Used to close resources from parent processes after fork
        (e.g. sockets/connections).
        """
        if self._closed:
            return
        self._closed = True
        dirty = self._dirty
        resource = self._resource
        while 1:  # - acquired
            try:
                dres = dirty.pop()
            except KeyError:
                break
            try:
                self.collect_resource(dres)
            except AttributeError:  # Issue #78
                pass
        while 1:  # - available
            # deque supports '.clear', but lists do not, so for that
            # reason we use pop here, so that the underlying object can
            # be any object supporting '.pop' and '.append'.
            try:
                res = resource.queue.pop()
            except IndexError:
                break
            try:
                self.collect_resource(res)
            except AttributeError:
                pass  # Issue #78

    def resize(self, limit, force=False, ignore_errors=False, reset=False):
        prev_limit = self._limit
        if (self._dirty and 0 < limit < self._limit) and not ignore_errors:
            if not force:
                raise RuntimeError(
                    "Can't shrink pool when in use: was={} now={}".format(
                        self._limit, limit))
            reset = True
        self._limit = limit
        if reset:
            try:
                self.force_close_all()
            except Exception:
                pass
        self.setup()
        if limit < prev_limit:
            self._shrink_down(collect=limit > 0)

    def _shrink_down(self, collect=True):
        class Noop:
            def __enter__(self):
                pass

            def __exit__(self, type, value, traceback):
                pass

        resource = self._resource
        # Items to the left are last recently used, so we remove those first.
        with getattr(resource, 'mutex', Noop()):
            while len(resource.queue) > self.limit:
                R = resource.queue.popleft()
                if collect:
                    self.collect_resource(R)

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, limit):
        self.resize(limit)

    if os.environ.get('KOMBU_DEBUG_POOL'):  # pragma: no cover
        _orig_acquire = acquire
        _orig_release = release

        _next_resource_id = 0
        # debug模式装饰一下原实现，增加打印信息

        def acquire(self, *args, **kwargs):  # noqa
            import traceback
            id = self._next_resource_id = self._next_resource_id + 1
            print(f'+{id} ACQUIRE {self.__class__.__name__}')
            r = self._orig_acquire(*args, **kwargs)
            r._resource_id = id
            print(f'-{id} ACQUIRE {self.__class__.__name__}')
            if not hasattr(r, 'acquired_by'):
                r.acquired_by = []
            r.acquired_by.append(traceback.format_stack())
            return r

        def release(self, resource):  # noqa
            id = resource._resource_id
            print(f'+{id} RELEASE {self.__class__.__name__}')
            r = self._orig_release(resource)
            print(f'-{id} RELEASE {self.__class__.__name__}')
            self._next_resource_id -= 1
            return r
