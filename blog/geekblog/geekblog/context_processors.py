import urlparse
from django.conf import settings
from django.core.urlresolvers import resolve, Resolver404


def urlname(request):
    full_path = request.get_full_path()
    parts = urlparse.urlparse(full_path)
    try:
        url_name = resolve(parts.path).url_name
    except Resolver404:
        url_name = full_path
    return {"url_name": url_name}


def website_meta(request):
    return {
        "saying": getattr(settings, "SAYING", ""),
        "site_name": getattr(settings, "WEBSITE_NAME", ""),
        "site_desc": getattr(settings, "WEBSITE_DESC", ""),
        "site_url": getattr(settings, "WEBSITE_URL", ""),
        "site_keywords": getattr(settings, "WEBSITE_KEYWORDS", ""),
        "blog_version": getattr(settings, "GEEKBLOG_VERSION", "1.3.4"),
        "duoshuo_short_name": getattr(settings, "DUOSHUO_SHORT_NAME", ""),
    }
