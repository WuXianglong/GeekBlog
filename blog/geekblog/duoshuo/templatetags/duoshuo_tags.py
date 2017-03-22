# -*- coding: utf-8 -*-
from django import template
# from django.conf import settings
from django.template import Library, Node

# DUOSHUO_SHORT_NAME = getattr(settings, "DUOSHUO_SHORT_NAME", None)
# DUOSHUO_SECRET = getattr(settings, "DUOSHUO_SECRET", None)

register = Library()


class DuoshuoCommentsNode(Node):

    def render(self, context):
        if context['is_mobile']:
            code = '''
            <div id="SOHUCS" sid="%s"></div>
            <script id="changyan_mobile_js" charset="utf-8" type="text/javascript" src="https://changyan.sohu.com/upload/mobile/wap-js/changyan_mobile.js?client_id=cysUkrlEx&conf=prod_7180d2fbed4a89dcc59f66a5cb9d91e0">
            </script>''' % context.get('id', '')
        else:
            code = '''
            <div id="SOHUCS" sid="%s" style="width: 692px"></div>
            <script charset="utf-8" type="text/javascript" src="https://changyan.sohu.com/upload/changyan.js"></script>
            <script type="text/javascript">
                window.changyan.api.config({
                    appid: 'cysUkrlEx',
                    conf: 'prod_7180d2fbed4a89dcc59f66a5cb9d91e0'
                });
            </script>''' % context.get('id', '')
        return code


def duoshuo_comments(parser, token):
    # short_name = token.contents.split()
    return DuoshuoCommentsNode()

duoshuo_comments = register.tag(duoshuo_comments)
