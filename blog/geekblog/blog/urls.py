from django.conf.urls import patterns, include, url

from blog.views import (show_homepage, show_article, show_category,
                        show_tag, show_search, show_archive_page, show_about_page, show_friend_link_page)


urlpatterns = patterns(
    '',
    url(r'^$', show_homepage, {'page_num': 1}, name='homepage'),
    url(r'^page/(?P<page_num>\d+)/$', show_homepage, name='homepage'),

    url(r'^article/(?P<slug>[a-z0-9A-Z_-]+)/$', show_article, name='article_detail'),
    url(r'^cate/(?P<cate_slug>[a-z_]+)(?:/(?P<page_num>\d+))?/$', show_category, name='category'),
    url(r'^tag/(?P<tag_slug>[a-z_]+)(?:/(?P<page_num>\d+))?/$', show_tag, name='tag'),
    url(r'^search/(?P<keyword>[^/]+)(?:/(?P<page_num>\d+))?/$', show_search, name='search'),

    url(r'^archive$', show_archive_page, name='archive_page'),
    url(r'^about$', show_about_page, name='about_page'),
    url(r'^friend$', show_friend_link_page, name='friend_link_page'),
)
