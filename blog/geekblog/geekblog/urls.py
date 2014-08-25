from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps import views as sitemap_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from blogcore.admin.sites import custom_site
from sitemap import ArticleSitemap
from blog.views import preview_article
from views import get_related_lookup_info, generate_verify_code, custom_page_not_found

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
    url(r'^console/article_preview/(?P<slug>[a-z0-9A-Z_-]+)/$', preview_article, name='article_preview'),
    url(r'^sitemap.xml$', cache_page(60 * 60 * 6)(sitemap_views.sitemap), {'sitemaps': {'articles': ArticleSitemap}}),
)

urlpatterns += staticfiles_urlpatterns()

handler404 = 'geekblog.geekblog.views.custom_page_not_found'
