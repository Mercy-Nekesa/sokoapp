from django.conf.urls import patterns, url

from .views import TimePeriodView

urlpatterns = patterns(
    '',
    url(r'^timeperiod/$', TimePeriodView.as_view(), name='time-period'),
)
