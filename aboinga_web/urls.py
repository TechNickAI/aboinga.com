from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from os import path
admin.autodiscover()


urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': path.join(settings.ROOT_PATH, 'static')}),
    (r'^(favicon.ico)', 'django.views.static.serve',
        {'document_root' : path.join(settings.ROOT_PATH, 'static', 'img')}),
    (r'^(robots.txt)', 'django.views.static.serve',
        {'document_root' : path.join(settings.ROOT_PATH, 'static')}),

    url(r'', include('aboinga_web.moments.urls')),

    url(r'^internal_admin/', include(admin.site.urls)),
)
