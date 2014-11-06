from django.conf.urls import patterns, include, url
from .views import SweepEntryDetail, SweepEntrySubmitted

urlpatterns = patterns('vodkamartinisweeps.views',
    url(r'^(?P<slug>[-\w]+)/thank-you/$', SweepEntrySubmitted.as_view(), name='vodkamartinisweeps_sweepentry_submitted'),
    url(r'^(?P<slug>[-\w]+)/$', SweepEntryDetail.as_view(), name='vodkamartinisweeps_sweepentry_detail'),
    # if we need to do something with the entry data
    #url(r'^(?P<slug>[-\w]+)/entry/(?P<sweepentry_pk>\d+)/$', SweepEntrySubmitted.as_view(), name='vodkamartinisweeps_sweepentry_submitted'),
)
