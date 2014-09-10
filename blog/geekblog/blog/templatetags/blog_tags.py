# -*- coding: UTF-8 -*-
from django import template

register = template.Library()


def render_article_item(item):
    return item

render_article_item = register.inclusion_tag('item.html')(render_article_item)


def render_mobile_article_item(item):
    return item

render_mobile_article_item = register.inclusion_tag('mobile/m_item.html')(render_mobile_article_item)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
