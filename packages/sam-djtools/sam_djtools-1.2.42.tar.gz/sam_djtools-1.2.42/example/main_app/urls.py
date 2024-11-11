from django.urls import re_path
from django.conf import settings
from django.contrib import admin
from django.views.static import serve


def define_pth():
    urls_prefix = settings.PATH_PREFIX or ''
    if urls_prefix:
        urls_prefix += '/'
    media_root = {'document_root': settings.MEDIA_ROOT}
    media_urls = [re_path(r'^' + urls_prefix + 'media/(?P<path>.*)$', serve, media_root)]

    static_root = {'document_root': settings.STATIC_ROOT}
    static_urls = [re_path(r'^' + urls_prefix + 'static/(?P<path>.*)$', serve, static_root)]

    # admin.autodiscover()
    if urls_prefix:
        urls_prefix = r'^'+urls_prefix
    app_urls = [
        re_path(urls_prefix + 'admin/', admin.site.urls),
    ]
    all_urls = media_urls + static_urls + app_urls
    return all_urls


urlpatterns = define_pth()
