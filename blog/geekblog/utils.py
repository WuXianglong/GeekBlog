# -*- coding: utf-8 -*-
import uuid
import json
import httplib
import logging
import datetime

from django.http import HttpResponse
from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError

logger = logging.getLogger('geekblog')

EPOCH = datetime.datetime(1970, 1, 1)
ONE_DAY = datetime.timedelta(days=1)

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


def total_seconds(delta):
    """return total seconds of a time delta."""
    if not isinstance(delta, datetime.timedelta):
        raise TypeError('delta must be a datetime.timedelta.')
    return delta.days * 86400 + delta.seconds + delta.microseconds / 1000000.0


def datetime2timestamp(dt):
    '''
    Converts a datetime object to UNIX timestamp in milliseconds.
    '''
    if isinstance(dt, datetime.datetime):
        timestamp = total_seconds(dt - EPOCH)
        return long(timestamp * 1000)
    return dt


def json_encode_datetime(obj):
    if hasattr(obj, 'utctimetuple'):
        return datetime2timestamp(obj)
    raise TypeError(repr(obj) + " is not JSON serializable")


def json_response(func):
    '''
    Wraps the return value of the parent as a JSON response.
    '''
    def json_responsed(*args, **kwargs):
        try:
            retval = func(*args, **kwargs)
        except Exception, e:
            logger.exception(e)
            retval = []
        if not isinstance(retval, HttpResponse):
            status_code = httplib.OK
            if isinstance(retval, dict) and 'http_status' in retval:
                status_code = retval.pop('http_status')
            content = json.dumps(retval, ensure_ascii=False, default=json_encode_datetime)
            response = HttpResponse(content, content_type='application/json; charset=utf-8', status=status_code)
        else:
            response = retval
        return response
    return json_responsed


class StringWithTitle(str):

    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self


class FreeConfigParser(SafeConfigParser):

    def _get(self, section, conv, option, default):
        return conv(self.get(section, option, default=default))

    def get(self, section, option, raw=False, vars=None, default=None):
        try:
            return SafeConfigParser.get(self, section, option, raw, vars)
        except (NoSectionError, NoOptionError), err:
            if default is not None:
                return default
            raise err

    def getint(self, section, option, default=None):
        return self._get(section, int, option, default)

    def getfloat(self, section, option, default=None):
        return self._get(section, float, option, default)

    def getboolean(self, section, option, default=None):
        try:
            return SafeConfigParser.getboolean(self, section, option)
        except (NoSectionError, NoOptionError), err:
            if default is not None:
                return default
            raise err
