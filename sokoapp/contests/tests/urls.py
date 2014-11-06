"""URLs to run the tests."""
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^test/', include('test_app.urls', namespace='test', app_name='test_app')),
    url(r'^admin/', include(admin.site.urls)),
)
