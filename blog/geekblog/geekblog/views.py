# -*- coding: utf-8 -*-
import logging

from django.contrib.auth.models import User, Group
from django.template import RequestContext
from django.shortcuts import render_to_response

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


def custom_page_not_found(request):
    template_name = 'mobile/m_404.html' if request.META.get('IS_MOBILE', False) else '404.html'
    return render_to_response(template_name, {}, context_instance=RequestContext(request))
