"""Entry-point for the :program:`celery` umbrella command."""

import sys

from . import maybe_patch_concurrency

__all__ = ('main',)


def main():
    """Entrypoint to the ``celery`` umbrella command."""
    """celery命令入口"""
    if 'multi' not in sys.argv:
        # multi指令处理
        maybe_patch_concurrency()
    # 具体执行的main函数
    from celery.bin.celery import main as _main
    sys.exit(_main())


if __name__ == '__main__':  # pragma: no cover
    main()
