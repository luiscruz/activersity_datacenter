from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

import datetime
from django.utils import timezone
import json

from datacenter.models import *
from django.contrib.auth.models import User

# Create your tests here.

def create_user(username, password):
    return User.objects.create_user(username, password = password)
    
def create_sensor(user, name):
    sensor = user.sensor_set.create(name = name)
    return sensor

class UserMethodTests(TestCase):
    def test_create_user(self):
        user = User(first_name='Test', last_name='User')
        user.save()
        user = User.objects.last();
        self.assertEqual([user.first_name, user.last_name], ['Test', 'User'])
                
class RestApiTests(APITestCase):
    def test_login(self):
        username = 'teste'
        password = 'password'
        test_user = create_user(username, password)
        data = {'username': username, 'password': password}
        json_data = json.dumps(data)
        response = self.client.post('/datacenter/login.json', data = json_data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(response.request.user, test_user)
        
    def test_wrong_login(self):
        username = 'teste'
        password = 'password'
        test_user = create_user(username, password)
        response = self.client.post('/datacenter/login/', {'username': username, 'password': 'wrong_password'})
        self.assertNotEqual(response.status_code, status.HTTP_200_OK, 'Status ok for wrong authentication')
        
    def test_logout(self):
        username = 'teste'
        password = 'password'
        test_user = create_user(username, password)
        login = self.client.login(username = username, password = password)
        self.assertTrue(login, 'Could not manually login user.')
        response = self.client.post('/datacenter/logout')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_upload_data(self):
        username = 'teste'
        password = 'password'
        test_user = create_user(username, password)
        login = self.client.login(username = username, password = password)
        sensor_name = 'sensor_test'
        sensor = create_sensor(test_user, sensor_name)
        data = {"data":  [
            {
                "value": {"x-axis":0.1,"y-axis":0.2,"z-axis":0.3},
                "date": "1291719228"
            },
            {
                "value": {"x-axis":0.3,"y-axis":0.2,"z-axis":0.5},
                "date": "1291719229"
            }
        ]}
        
        json_data = json.dumps(data)
        response = self.client.post('/datacenter/sensors/'+str(sensor.id)+'/data.json', data = json_data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest' )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(sensor.sensordata_set.all()), 2)
        
    def test_upload_data_without_date(self):
        username = 'teste'
        password = 'password'
        test_user = create_user(username, password)
        login = self.client.login(username = username, password = password)
        sensor_name = 'sensor_test'
        sensor = create_sensor(test_user, sensor_name)
        data = {"data":  [
            {
                "value": {"x-axis":0.1,"y-axis":0.2,"z-axis":0.3},
            }
        ]}
        
        json_data = json.dumps(data)
        response = self.client.post('/datacenter/sensors/'+str(sensor.id)+'/data.json', data = json_data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest' )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_upload_data_for_multiple_sensors(self):
        username = 'teste'
        password = 'password'
        test_user = create_user(username, password)
        login = self.client.login(username = username, password = password)
        sensor_name = 'sensor_test'
        sensor = create_sensor(test_user, sensor_name)

        data = {
          "sensors": [
            {
              "data": [
                {
                  "value": {"x-axis":0.1,"y-axis":0.2,"z-axis":0.3},
                  "date": "1291719228"
                },
                {
                  "value": {"x-axis":0.3,"y-axis":0.2,"z-axis":0.5},
                  "date": "1291719229"
                }
              ],
              "sensor_id": sensor.id
            }
          ]
        }
        
        json_data = json.dumps(data)
        response = self.client.post('/datacenter/sensors/data.json', data = json_data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest' )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(sensor.sensordata_set.all()), 2)
        
    def test_get_data_from_sensor(self):
        username = 'teste'
        password = 'password'
        test_user = create_user(username, password)
        login = self.client.login(username = username, password = password)
        sensor_name = 'sensor_test'
        sensor = create_sensor(test_user, sensor_name)
        
        #generate data
        sensor.sensordata_set.create(created_at = timezone.now(), data = {'a': 2})
        sensor.sensordata_set.create(created_at = timezone.now(), data = {'a': 4})        
        
        response = self.client.get('/datacenter/sensors/'+str(sensor.id)+'/data.json', {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data.get('data')), 2)
        
    def test_create_sensor(self):
        username = 'teste'
        password = 'password'
        sensor_name = 'sensor_test'
        test_user = create_user(username, password)
        login = self.client.login(username = username, password = password)
        sensor_data = {'sensor': {'name': sensor_name}}
        json_data = json.dumps(sensor_data)
        response = self.client.post('/datacenter/sensors.json', data = json_data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Response status is not 201')
        data = json.loads(response.content)
        
        sensor_id = data.get('sensor').get('id')
        self.assertIsNotNone(sensor_id, 'Sensor id is not present in response')
        sensor = Sensor.objects.get(id=sensor_id)
        self.assertIsNotNone(sensor, 'Sensor with the provided id is not found')
        self.assertEqual(sensor.user, test_user, 'Sensor user is not the authenticated user')
        self.assertEqual(sensor.name, sensor_name, 'Sensor name was not stored')
        
    def test_list_sensors(self):
        username = 'teste'
        password = 'password'
        test_user = create_user(username, password)
        login = self.client.login(username = username, password = password)
        sensor_name = 'sensor_test'
        sensor = create_sensor(test_user, sensor_name)
        
        response = self.client.get('/datacenter/sensors', {})
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'List sensors did not return 200')
        data = json.loads(response.content)
        self.assertEqual(data.get('sensors')[0].get('id'), sensor.id, 'List sensors did not provide a good response')
        
    def test_register_user_json(self):
        username = 'janjager'
        password = 'password'
        #import hashlib
        #password_md5 = hashlib.md5( password ).hexdigest()
        user_data = {
            "user": {
                "username": username,
                "email": "jan@test.nl",
                "name": "Jan",
                "surname": "Jager",
                "password": password,
                "mobile": "0031612345678"
            }
        }
        json_data = json.dumps(user_data)
        response = self.client.post('/datacenter/users.json', data = json_data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Create user did not return 201')
        login = self.client.login(username = username, password = password)
        self.assertTrue(login, 'Could not login registered user.')

    def test_register_user_with_minimum_fields_json(self):
        username = 'janjager'
        password = 'password'
        import hashlib
        password_md5 = hashlib.md5( password ).hexdigest()
        user_data = {
            "user": {
                "username": username,
                "email": "jan@test.nl",
                "password": password_md5,
            }
        }
        json_data = json.dumps(user_data)
        response = self.client.post('/datacenter/users.json', data = json_data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Create user did not return 201')
        
    def test_add_sensor_to_device(self):
        username = 'teste'
        password = 'password'
        test_user = create_user(username, password)
        login = self.client.login(username = username, password = password)
        sensor_name = 'sensor_test'
        sensor = create_sensor(test_user, sensor_name)
        
        device_type = 'iPhone Simulator'
        device_uuid = '620A033F-4738-4319-AAC8-0F27B310AA82'
        request_data = {'device': {'type': device_type, 'uuid': device_uuid}}
        json_data = json.dumps(request_data)
        
        response = self.client.post('/datacenter/sensors/'+str(sensor.id)+'/device', data = json_data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        sensor = Sensor.objects.get(id = sensor.id)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Create user did not return 201')
        self.assertIsNotNone(sensor.device)
        self.assertEqual(sensor.device.uuid, device_uuid)
        #self.assertEqual(sensor.device_type, '1')
    