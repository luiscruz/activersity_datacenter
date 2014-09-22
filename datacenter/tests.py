from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

import datetime
from django.utils import timezone

from datacenter.models import *
from django.contrib.auth.models import User

# Create your tests here.


class UserMethodTests(TestCase):
    def test_create_user(self):
        user = User(first_name='Test', last_name='User')
        user.save()
        user = User.objects.last();
        self.assertEqual([user.first_name, user.last_name], ['Test', 'User'])
                
class RestApiTests(APITestCase):
    def test_login(self):
        response = self.client.post('/datacenter/login/', {'username': 'username', 'password': 'password_md5'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertIn('x-session_id', response.data.keys())
        
    def test_logout(self):
        response = self.client.post('/datacenter/logout/', {'x-session_id': 'fixme'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_upload_data(self):
        sensor_id = 1
        session_id = 'FIXME'
        response = self.client.post('/datacenter/sensors/'+str(sensor_id)+'/data.json', {'x-session_id': session_id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_data_from_sensor(self):
        sensor_id = 1
        session_id = 'FIXME'
        response = self.client.get('/datacenter/sensors/'+str(sensor_id)+'/data.json', {'x-session_id': session_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_sensor(self):
        session_id = 'FIXME'
        response = self.client.get('/datacenter/sensors.json', {'x-session_id': session_id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.ass
        
    #def test_register_user(self):
        
