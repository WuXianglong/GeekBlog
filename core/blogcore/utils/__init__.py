#! -*- coding:utf-8 -*-
import uuid

SIZE_UNIT = {"BYTE": 1, "KB": 1024, "MB": 1048576, "GB": 1073741824, "TB": 1099511627776L}


def friendly_size(size):
    if size < SIZE_UNIT["KB"]:
        unit = "BYTE"
    elif size < SIZE_UNIT["MB"]:
        unit = "KB"
    elif size < SIZE_UNIT["GB"]:
        unit = "MB"
    elif size < SIZE_UNIT["TB"]:
        unit = "GB"
    else:
        unit = "TB"

    if size % SIZE_UNIT[unit] == 0:
        return "%s%s" % (size / SIZE_UNIT[unit], unit)
    else:
        return "%0.2f%s" % (round(float(size) / float(SIZE_UNIT[unit]), 2), unit)


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def generate_unique_token():
    token = str(uuid.uuid4())
    return token.replace('-', '')


class StringWithTitle(str):

    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self
