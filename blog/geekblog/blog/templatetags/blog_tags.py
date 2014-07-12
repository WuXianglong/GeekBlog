#-*- coding: UTF-8 -*-
from django import template

register = template.Library()


def render_article_item(item):
    return item

render_article_item = register.inclusion_tag('item.html')(render_article_item)
