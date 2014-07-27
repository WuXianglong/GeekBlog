"""
leftnav template tags, the following leftnav tags are available:

 * ``{% admin_tools_render_leftnav %}``
 * ``{% admin_tools_render_leftnav_item %}``
 * ``{% admin_tools_render_leftnav_css %}``

To load the leftnav tags in your templates: ``{% load admin_tools_leftnav_tags %}``.
"""

from django import template
from django.core.urlresolvers import reverse

from admin_tools.utils import get_media_url, get_admin_site_name
from admin_tools.theming import items
from admin_tools.theming.leftnav import DefaultLeftNav

register = template.Library()
tag_func = register.inclusion_tag('admin_tools/leftnav/dummy.html', takes_context=True)


def admin_tools_render_leftnav(context, leftnav=None):
    """
    Template tag that renders the leftnav, it takes an optional ``nav`` instance
    as unique argument, if not given, the leftnav will be retrieved with the
    ``get_admin_leftnav`` function.
    """
    if leftnav is None:
        leftnav = DefaultLeftNav()

    leftnav.init_with_context(context)

    context.update({
        'template': leftnav.template,
        'leftnav': leftnav,
    })
    return context
admin_tools_render_leftnav = tag_func(admin_tools_render_leftnav)


def admin_tools_render_leftnav_item(context, item, index=None, singal_child=False):
    """
    Template tag that renders a given leftnav item, it takes a ``LeftNavItem``
    instance as unique parameter.
    """
    item.init_with_context(context)

    context.update({
        'template': item.template,
        'item': item,
        'index': index,
        'singal_child': singal_child,
        'selected': item.is_selected(context['request']),
    })
    return context
admin_tools_render_leftnav_item = tag_func(admin_tools_render_leftnav_item)


def admin_tools_render_leftnav_css(context, leftnav=None):
    """
    Template tag that renders the leftnav css files,, it takes an optional
    ``LeftNav`` instance as unique argument, if not given, the leftnav will be
    retrieved with the ``get_admin_leftnav`` function.
    """
    if leftnav is None:
        leftnav = DefaultLeftNav()

    context.update({
        'template': 'admin_tools/leftnav/css.html',
        'css_files': leftnav.Media.css,
        'media_url': get_media_url(),
    })
    return context
admin_tools_render_leftnav_css = tag_func(admin_tools_render_leftnav_css)
