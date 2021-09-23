"""Promises, promises, promises."""
import re

from collections import namedtuple

from .abstract import Thenable
from .promises import promise
from .synchronization import barrier
from .funtools import (
    maybe_promise, ensure_promise,
    ppartial, preplace, starpromise, transform, wrap,
)


__version__ = '5.0.0'
__author__ = 'Ask Solem'
__contact__ = 'ask@celeryproject.org'
__homepage__ = 'http://github.com/celery/vine'
__docformat__ = 'restructuredtext'

# -eof meta-
# 可命名元祖
version_info_t = namedtuple('version_info_t', (
    'major', 'minor', 'micro', 'releaselevel', 'serial',
))
# bump version can only search for {current_version}
# so we have to parse the version here.
# 使用正则匹配出版本号。
# 4个分组，最后一个分组使用?,表示可有可无；前三个分组是纯数字，使用.隔开；最后的分组是任意字符,比如5.0.0a1这样的版本中的a1
_temp = re.match(
    r'(\d+)\.(\d+).(\d+)(.+)?', __version__).groups()
VERSION = version_info = version_info_t(
    int(_temp[0]), int(_temp[1]), int(_temp[2]), _temp[3] or '', '')
# 清理
del(_temp)
del(re)

__all__ = [
    'Thenable', 'promise', 'barrier',
    'maybe_promise', 'ensure_promise',
    'ppartial', 'preplace', 'starpromise', 'transform', 'wrap',
]
