"""Scheduling Utilities."""

from itertools import count

from .imports import symbol_by_name

__all__ = (
    'FairCycle', 'priority_cycle', 'round_robin_cycle', 'sorted_cycle',
)

CYCLE_ALIASES = {
    'priority': 'kombu.utils.scheduling:priority_cycle',
    'round_robin': 'kombu.utils.scheduling:round_robin_cycle',
    'sorted': 'kombu.utils.scheduling:sorted_cycle',
}


class FairCycle:
    """Cycle between resources.

    Consume from a set of resources, where each resource gets
    an equal chance to be consumed from.

    Arguments:
        fun (Callable): Callback to call.
        resources (Sequence[Any]): List of resources.
        predicate (type): Exception predicate.
    """
    """从头部到尾部的公平循环"""

    def __init__(self, fun, resources, predicate=Exception):
        self.fun = fun
        self.resources = resources
        self.predicate = predicate
        #  初始位置
        self.pos = 0

    def _next(self):
        while 1:
            try:
                resource = self.resources[self.pos]
                # 位置加1
                self.pos += 1
                return resource
            except IndexError:
                # 到尾部后，重置位置
                self.pos = 0
                if not self.resources:
                    raise self.predicate()

    def get(self, callback, **kwargs):
        """Get from next resource."""
        # 无限重试
        for tried in count(0):  # for infinity
            # 获取资源
            resource = self._next()
            try:
                # 利用资源
                return self.fun(resource, callback, **kwargs)
            except self.predicate:
                # 容错上限
                # reraise when retries exchausted.
                if tried >= len(self.resources) - 1:
                    raise

    def close(self):
        """Close cycle."""

    def __repr__(self):
        """``repr(cycle)``."""
        return '<FairCycle: {self.pos}/{size} {self.resources}>'.format(
            self=self, size=len(self.resources))


class round_robin_cycle:
    """Iterator that cycles between items in round-robin."""
    """轮询调度算法"""

    def __init__(self, it=None):
        self.items = it if it is not None else []

    def update(self, it):
        """Update items from iterable."""
        """更新列表"""
        self.items[:] = it

    def consume(self, n):
        """Consume n items."""
        """消费n个元素"""
        return self.items[:n]

    def rotate(self, last_used):
        """Move most recently used item to end of list."""
        """旋转:把最后一个元素放到列表某尾"""
        items = self.items
        try:
            items.append(items.pop(items.index(last_used)))
        except ValueError:
            pass
        return last_used


class priority_cycle(round_robin_cycle):
    """Cycle that repeats items in order."""
    """优先队列，列表按照优先级排序，不用动态变化"""

    def rotate(self, last_used):
        """Unused in this implementation."""


class sorted_cycle(priority_cycle):
    """Cycle in sorted order."""

    def consume(self, n):
        """Consume n items."""
        """重新排序"""
        return sorted(self.items[:n])


def cycle_by_name(name):
    """Get cycle class by name."""
    return symbol_by_name(name, CYCLE_ALIASES)
