#! -*- coding:utf-8 -*-
import uuid


def friendly_size(size):
    if size < 1024:
        size = '%sB' % size
    elif size >= 1024 and size < 1024 * 1024:   # 1KB ~ 1M
        size = '%sK' % size * 1.0 / 1024
    elif size >= 1024 * 1024:
        size = '%sM' % size * 1.0 / (1024 * 1024)
    parts = size.split('.')
    if len(parts) > 1:
        if parts[1][0] == '0':
            size = parts[0] + parts[1][-1]
        else:
            size = '%s.%s%s' % (parts[0], parts[1][0], parts[1][-1])
    return size


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except Exception:
        return default


def generate_unique_token():
    token = str(uuid.uuid4())
    return token.replace('-', '')


class string_with_title(str):

    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self
