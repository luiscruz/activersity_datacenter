from django.test import TestCase

import datetime
from django.utils import timezone

from datacenter.models import User, ActivityLog
# Create your tests here.


class UserMethodTests(TestCase):
    def test_create_user(self):
        user = User(first_name='Test', last_name='User')
        user.save()
        user = User.objects.last();
        self.assertEqual([user.first_name, user.last_name], ['Test', 'User'])
        
    def test_add_activitylog_entry(self):
        user = User(first_name='Test', last_name='User')
        user.save()
        data = {'created_at': timezone.now() ,'sensor_type': 1, 'sensor_name': 'GPS TomTom', 'data_type':'WGS84', 'latitude': 41.17930404773651, 'longitude': -8.595282847981604}
        activity_log = user.add_activitylog(data)
        self.assertEqual(user.activitylog_set.count(), 1)
        self.assertEqual(ActivityLog.objects.last(), user.activitylog_set.last(), activity_log)

    def test_add_activity_log_entry_with_data(self):
        user = User(first_name='Test', last_name='User')
        user.save()
        data = {'created_at': timezone.now() ,'sensor_type': 1, 'sensor_name': 'GPS TomTom', 'data_type':'WGS84', 'latitude': 41.17930404773651, 'longitude': -8.595282847981604}
        user.add_activitylog(data)
        self.assertEqual(ActivityLog.objects.last().data['sensor_name'], "GPS TomTom")