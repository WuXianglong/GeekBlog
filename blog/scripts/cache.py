# -*- coding: UTF-8 -*-
import hashlib

from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest
from django.utils.cache import get_cache_key
from django.utils.encoding import iri_to_uri
from django.utils.translation import get_language


def expire_page(path):
    request = HttpRequest()
    request.path = path
    key = get_cache_key(request)
    if cache.has_key(key):
        cache.delete(key)


def url_cache_key(url, language=None, key_prefix=None):
    if key_prefix is None:
        key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX
    ctx = hashlib.md5()
    path = hashlib.md5(iri_to_uri(url))
    cache_key = 'views.decorators.cache.cache_page.%s.%s.%s.%s' % (
        key_prefix, 'GET', path.hexdigest(), ctx.hexdigest())
    if settings.USE_I18N:
        cache_key += '.%s' % (language or get_language())
    return cache_key


if __name__ == "__main__":
    expire_page("/friend")
    expire_page("/about")
