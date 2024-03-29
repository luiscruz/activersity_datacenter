from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from datacenter.views import *

urlpatterns = patterns('datacenter.views',
    # url(r'^users/$', UserList.as_view()),
    # url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
    # url(r'^activitylogs/$', ActivityLogList.as_view()),
    # url(r'^activitylogs/(?P<pk>[0-9]+)/$', ActivityLogDetail.as_view()),
    
    url(r'^login$', login),
    url(r'^logout$', logout),
    url(r'^sensors/(?P<pk>[0-9]+)/data$', SensorsDataView.as_view()),
    url(r'^sensors/(?P<pk>[0-9]+)/device$', sensor_device),
    url(r'^sensors/data$', upload_data_for_multiple_sensors),
    url(r'^sensors$', SensorsView.as_view()),
    url(r'^test$', test),
    
    ##Users
    url(r'^users$', users),
    url(r'^users/(?P<user_id>[0-9]+)$', users_show),
    
    ## Analytics ##
    url(r'^basic_analytics$', basic_analytics),
    url(r'^data_uploaded_per_day$', data_uploaded_per_day),
    
)

urlpatterns = format_suffix_patterns(urlpatterns)