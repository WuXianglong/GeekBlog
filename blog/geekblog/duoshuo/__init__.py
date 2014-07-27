# -*- coding:utf-8 -*-
#!/usr/bin/env python
#
# Copyright 2012 Duoshuo
#
__version__ = '0.1'

import os
import urllib
import urllib2
import warnings
import urlparse
import hashlib
import httplib

try:
    import json
    _parse_json = lambda s: json.loads(s)
except ImportError:
    try:
        import simplejson
        _parse_json = lambda s: simplejson.loads(s)
    except ImportError:
        from django.utils import simplejson
        _parse_json = lambda s: simplejson.loads(s)

try:
    import Cookie
except ImportError:
    import https.cookies as cookie

HOST = 'api.duoshuo.com'
URI_SCHEMA = 'http'
INTERFACES = _parse_json(open(os.path.join(os.path.dirname(__file__), 'interfaces.json'), 'r').read())

try:
    import settings
except ImportError:
    DUOSHUO_SHORT_NAME = None
    DUOSHUO_SECRET = None
else:
    DUOSHUO_SHORT_NAME = getattr(settings, "DUOSHUO_SHORT_NAME", None)
    DUOSHUO_SECRET = getattr(settings, "DUOSHUO_SECRET", None)


class APIError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return '%s: %s' % (self.code, self.message)


class Resource(object):

    def __init__(self, api, interface=INTERFACES, node=None, tree=()):
        self.api = api
        self.node = node
        self.interface = interface
        if node:
            tree = tree + (node,)
        self.tree = tree

    def __getattr__(self, attr):
        if attr in getattr(self, '__dict__'):
            return getattr(self, attr)
        interface = self.interface
        if attr not in interface:
            interface[attr] = {}
            #raise APIError('03', 'Interface is not defined')
        return Resource(self.api, interface[attr], attr, self.tree)

    def __call__(self, **kwargs):
        return self._request(**kwargs)

    def _request(self, **kwargs):

        resource = self.interface
        for k in resource.get('required', []):
            if k not in [x.split(':')[0] for x in kwargs.keys()]:
                raise ValueError('Missing required argument: %s' % k)

        method = kwargs.pop('method', resource.get('method'))

        api = self.api

        format = kwargs.pop('format', api.format)
        path = '%s://%s/%s.%s' % (URI_SCHEMA, HOST, '/'.join(self.tree), format)

        if 'secret' not in kwargs and api.secret:
            kwargs['secret'] = api.secret
        if 'short_name' not in kwargs and api.short_name:
            kwargs['short_name'] = api.short_name
        # We need to ensure this is a list so that
        # multiple values for a key work
        params = []
        for k, v in kwargs.iteritems():
            if isinstance(v, (list, tuple)):
                for val in v:
                    params.append((k, val))
            else:
                params.append((k, v))

        if method == 'GET':
            path = '%s?%s' % (path, urllib.urlencode(params))
            response = urllib2.urlopen(path).read()
        else:
            data = urllib.urlencode(params)
            response = urllib2.urlopen(path, data).read()

        try:
            return _parse_json(response)
        except:
            return _parse_json('{"code": "500"}')


class DuoshuoAPI(Resource):
    def __init__(self, short_name=DUOSHUO_SHORT_NAME, secret=DUOSHUO_SECRET, format='json', **kwargs):
        self.short_name = short_name
        self.secret = secret
        self.format = format

        self.uri_schema = URI_SCHEMA
        self.host = HOST

        if not secret or not short_name:
            warnings.warn('You should pass short_name and secret.')
        # self.version = version
        super(DuoshuoAPI, self).__init__(self)

    def _request(self, **kwargs):
        raise SyntaxError('You cannot call the API without a resource.')

    def _get_key(self):
        return self.secret
    key = property(_get_key)

    def get_token(self, code=None):
        if not code:
            raise APIError('01', 'Invalid request: code')
        #elif not redirect_uri:
        #    raise APIError('01', 'Invalid request: redirect_uri')
        else:
            #params = {'client_id': self.client_id, 'secret': self.secret, 'redirect_uri': redirect_uri, 'code': code}
            params = {'code': code}
            data = urllib.urlencode(params)
            url = '%s://%s/oauth2/access_token' % (URI_SCHEMA, HOST)
            print url
            request = urllib2.Request(url)
            response = urllib2.build_opener(urllib2.HTTPCookieProcessor()).open(request, data)

            return _parse_json(response.read())

    def setSecret(self, key):
        self.secret = key

    def setFormat(self, key):
        self.format = key
