# -*- coding: utf-8 -*-
import logging

from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import requires_csrf_token
from django.template import TemplateDoesNotExist, RequestContext

from blog.models import *
from utils import json_response
from blogcore.utils.verify_code import VerifyCode

logger = logging.getLogger('geekblog')


@json_response
def get_related_lookup_info(request):
    request_get = request.GET
    lookup_cls = request_get.get('cls_name', '')
    lookup_value = request_get.get('v', '')
    if not lookup_cls or not lookup_value:
        logger.exception('Invaild params, url: %s, field: %s, value: %s' % (lookup_cls, lookup_value))
        return ''

    try:
        obj = eval(lookup_cls).objects.get(pk__exact=lookup_value)
    except Exception:
        obj = None
    return str(obj) if obj else ''


def generate_verify_code(request):
    return VerifyCode(request).display()


@requires_csrf_token
def custom_page_not_found(request, template_name='404.html'):
    if request.META.get('IS_MOBILE', False):
        template_name = 'mobile/404.html'

    try:
        template = loader.get_template(template_name)
        content_type = None             # Django will use DEFAULT_CONTENT_TYPE
    except TemplateDoesNotExist:
        template = Template(
            '<h1>Not Found</h1>'
            '<p>The requested URL {{ request_path }} was not found on this server.</p>')
        content_type = 'text/html'
    body = template.render(RequestContext(request, {'request_path': request.path}))
    return http.HttpResponseNotFound(body, content_type=content_type)
