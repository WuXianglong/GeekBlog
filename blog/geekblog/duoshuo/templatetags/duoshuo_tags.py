# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.template import Library, Node

DUOSHUO_SHORT_NAME = getattr(settings, "DUOSHUO_SHORT_NAME", None)
DUOSHUO_SECRET = getattr(settings, "DUOSHUO_SECRET", None)

register = Library()


class DuoshuoCommentsNode(Node):

    def __init__(self, short_name=DUOSHUO_SHORT_NAME):
        self.short_name = short_name

    def render(self, context):
        code = '''<!-- Duoshuo Comment BEGIN -->
        <div class="ds-thread" id="ds-thread" data-thread-key="%s" data-title="%s" data-url="%s"></div>
        <script type="text/javascript">
        var duoshuoQuery = {short_name: "%s"};
        (function() {
            var ds = document.createElement('script');
            ds.type = 'text/javascript';ds.async = true;
            ds.src = 'http://static.duoshuo.com/embed.js';
            ds.charset = 'UTF-8';
            (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(ds);
        })();
        </script>
        <!-- Duoshuo Comment END -->''' % (context.get('id', ''), context.get('page_title', ''),
                context['request'].build_absolute_uri(), self.short_name)
        return code


def duoshuo_comments(parser, token):
    short_name = token.contents.split()

    if DUOSHUO_SHORT_NAME:
        return DuoshuoCommentsNode(DUOSHUO_SHORT_NAME)
    elif len(short_name) == 2:
        return DuoshuoCommentsNode(short_name[1])
    else:
        raise template.TemplateSyntaxError, 'duoshuo_comments tag takes SHORT_NAME as exactly one argument'

duoshuo_comments = register.tag(duoshuo_comments)
