"""
Module where admin tools leftnav classes are defined.
"""
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from admin_tools.theming import items


class LeftNav(object):
    """
    This is the base class for creating custom navigation leftnavs.
    A leftnav can have the following properties:

    ``template``
        A string representing the path to template to use to render the leftnav.
        As for any other template, the path must be relative to one of the
        directories of your ``TEMPLATE_DIRS`` setting.
        Default value: "admin_tools/leftnav/leftnav.html".

    ``children``
        A list of children leftnav items. All children items mus be instances of
        the :class:`~admin_tools.leftnav.items.LeftNavItem` class.

    If you want to customize the look of your leftnav and it's leftnav items, you
    can declare css stylesheets and/or javascript files to include when
    rendering the leftnav, for example::

        from admin_tools.leftnav import LeftNav

        class MyLeftNav(LeftNav):
            class Media:
                css = ('/media/css/myleftnav.css',)
                js = ('/media/js/myleftnav.js',)

    Here's a concrete example of a custom leftnav::

        from django.core.urlresolvers import reverse
        from admin_tools.leftnav import items, LeftNav

        class MyLeftNav(LeftNav):
            def __init__(self, **kwargs):
                super(MyLeftNav, self).__init__(**kwargs)
                self.children += [
                    items.LeftNavItem('Home', reverse('admin:index')),
                    items.AppList('Applications'),
                    items.LeftNavItem('Multi level leftnav item',
                        children=[
                            items.LeftNavItem('Child 1', '/foo/'),
                            items.LeftNavItem('Child 2', '/bar/'),
                        ]
                    ),
                ]

    Below is a screenshot of the resulting leftnav:

    .. image:: images/leftnav_example.png
    """
    template = 'admin_tools/leftnav/leftnav.html'
    children = None

    class Media:
        css = ()
        js = ()

    def __init__(self, **kwargs):
        for key in kwargs:
            if hasattr(self.__class__, key):
                setattr(self, key, kwargs[key])
        self.children = kwargs.get('children', [])

    def init_with_context(self, context):
        """
        Sometimes you may need to access context or request variables to build
        your leftnav, this is what the ``init_with_context()`` method is for.
        This method is called just before the display with a
        ``django.template.RequestContext`` as unique argument, so you can
        access to all context variables and to the ``django.http.HttpRequest``.
        """
        pass


class DefaultLeftNav(LeftNav):
    """
    The default leftnav displayed by django-admin-tools.
    To change the default leftnav you'll have to type the following from the
    commandline in your project root directory::

        python manage.py customleftnav

    And then set the ``ADMIN_TOOLS_LEFTNAV`` settings variable to point to your
    custom leftnav class.
    """

    def init_with_context(self, context):
        for k in sorted(settings.LEFT_NAV_MODELS.keys(), key=lambda k: settings.LEFT_NAV_MODELS[k]['order']):
            v = settings.LEFT_NAV_MODELS[k]
            app_list = items.AppList(v['title'], models=v['models'], \
                    app_label_order=v['app_label_order'])
            self.children += [app_list]
