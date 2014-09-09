# -*- coding:utf-8 -*-
#!/usr/bin/env python
import jwt
import hmac
import time
import json
import base64
import urllib
import urllib2
import hashlib

from django.conf import settings


def remote_auth(user_id, name, email, url=None, avatar=None, DUOSHUO_SECRET=None):
    """
    实现Remote Auth后可以在评论框显示本地身份(已停用，由set_duoshuo_token代替)
    Use:
        views.py: sig = remote_auth(key=request.user.id, name=request.user.username, email=request.user.email)
        template/xxx.html: duoshuoQuery['remote_auth'] = {{ sig }}
    """
    data = json.dumps({
        'key': user_id,
        'name': name,
        'email': email,
        'url': url,
        'avatar': avatar,
    })
    message = base64.b64encode(data)
    timestamp = int(time.time())
    sig = hmac.HMAC(settings.DUOSHUO_SECRET, '%s %s' % (message, timestamp), hashlib.sha1).hexdigest()
    duoshuo_query = '%s %s %s' % (message, sig, timestamp)
    return duoshuo_query


def set_duoshuo_token(request, response):
    """
    在评论框显示本地身份
    Use:
        from utils import set_duoshuo_token
        response = HttpResponse()
        return set_duoshuo_token(request, response)

    """
    if (request.user.id):
        token = {
            'short_name': settings.DUOSHUO_SHORT_NAME,
            'user_key': request.user.id,
            'name': request.user.username,
        }
        signed_token = jwt.encode(token, settings.DUOSHUO_SECRET)
        response.set_cookie('duoshuo_token', signed_token)
    return response


def get_url(api, redirect_uri=None):
    if not redirect_uri:
        raise ValueError('Missing required argument: redirect_uri')
    else:
        params = {'client_id': api.short_name, 'redirect_uri': redirect_uri, 'response_type': 'code'}
        return '%s://%s/oauth2/%s?%s' % (api.uri_schema, api.host, 'authorize', \
            urllib.urlencode(sorted(params.items())))


def sync_comment(posts):
    api_url = 'http://56we.duoshuo.com/api/import/comments.json'
    data = urllib.urlencode({
       'data': posts,
    })
    response = json.loads(urllib2.urlopen(api_url, data).read())
