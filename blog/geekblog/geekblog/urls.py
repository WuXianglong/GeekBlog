from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from blogcore.admin.sites import custom_site
from views import get_related_lookup_info, generate_verify_code

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

js_info_dict = {
    'packages': ('geekblog.jsi18n',),
}

urlpatterns = patterns('',
    url(r'^', include('blog.urls')),
    url(r'^ueditor/', include('ueditor.urls')),
    url(r'^console/', include(custom_site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    url(r'^console/get_related_lookup_info', get_related_lookup_info, name='get_related_lookup_info'),

    url(r'^verify_code', generate_verify_code, name='generate_verify_code'),
)

urlpatterns += staticfiles_urlpatterns()
