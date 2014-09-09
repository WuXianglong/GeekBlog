# -*- coding: utf-8 -*-
import json
import httplib
import logging
import datetime
from django.http import HttpResponse
from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError

logger = logging.getLogger('geekblog')

EPOCH = datetime.datetime(1970, 1, 1)
ONE_DAY = datetime.timedelta(days=1)


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
