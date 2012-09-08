from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    # One for public, one for private
    (r'^moment/not-public/(?P<slug>.*)$', 'aboinga_web.moments.views.detail', {'public_path': False}),
    (r'^moment/(?P<slug>.*)$', 'aboinga_web.moments.views.detail', {'public_path': True}),
    (r'^about', 'aboinga_web.moments.views.about'),
    (r'^$', 'aboinga_web.moments.views.home'),
)
