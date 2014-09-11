from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from datacenter.views import *

urlpatterns = patterns('datacenter.views',
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
    url(r'^activitylogs/$', ActivityLogList.as_view()),
    url(r'^activitylogs/(?P<pk>[0-9]+)/$', ActivityLogDetail.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)