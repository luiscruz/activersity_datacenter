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
    
def set_as_superuser(user):
    user.is_superuser = True
    user.is_staff = True
    user.save()

def create_superuser(username, password):
    superuser = create_user(username, password)
    set_as_superuser(superuser)
    return superuser
    
def create_sensor(user, name):
    sensor = user.sensor_set.create(name = name)
    return sensor
def create_device(device_type, device_uuid):
    device = Device.objects.create(device_type = device_type, uuid = device_uuid)
    return device


class UserMethodTests(TestCase):
    def test_create_user(self):
        user = User(first_name='Test', last_name='User')
        user.save()
        user = User.objects.last();
        self.assertEqual([user.first_name, user.last_name], ['Test', 'User'])
    
    def test_data_from_sensor_with_type(self):
        username = 'teste'
        password = 'password'
        test_user = create_user(username, password)
        test_user = UserWithExtraMethods.objects.get(id = test_user.id)
        
        device_type = 'test_sensor'
        sensor_one = test_user.sensor_set.create(name = 'test_sensor_one', device_type = device_type)
        sensor_two = test_user.sensor_set.create(name = 'test_sensor_two', device_type = device_type)
        sensor_three = test_user.sensor_set.create(name = 'test_sensor_three', device_type = 'other_type')
        
        # Data from test_sensor sensors:
        sensor_one.sensordata_set.create(data = 'test_data')
        sensor_one.sensordata_set.create(data = 'test_data')
        sensor_two.sensordata_set.create(data = 'test_data')
        # Data from 'other_type' sensors:
        sensor_three.sensordata_set.create(data = 'test_data')
        
        sensor_data = test_user.data_from_sensor_with_type(device_type)
        self.assertIsNotNone(sensor_data)
        self.assertEqual(sensor_data.count(), 3)
        
    def test_noise_timeline(self):
        test_user = create_user('teste', 'password')
        test_user = UserWithExtraMethods.objects.get(id = test_user.id)
        
        sensor = test_user.sensor_set.create(name = 'test_sensor_one', device_type = 'noise_sensor')
        sensordata = sensor.sensordata_set.create(data = {"value": -1})
        
        timeline = test_user.noise_timeline()
        self.assertEqual(len(timeline), 1)
        self.assertEqual(timeline[0] ,{'created_at': sensordata.created_at, 'data':'{"value":-1}'})
        
    def test_devices_count(self):
        test_user = create_user('teste', 'password')
        test_user = UserWithExtraMethods.objects.get(id = test_user.id)
        self.assertEqual(test_user.devices_count(), 0);
        
        sensor_name = 'sensor_test'
        sensor = create_sensor(test_user, sensor_name)
        device_type = 'iPhone Simulator'
        device_uuid = '620A033F-4738-4319-AAC8-0F27B310AA82'
        device = create_device(device_type, device_uuid)
        device.sensor_set.add(sensor)
        self.assertEqual(test_user.devices_count(), 1);
        
        
class SensorDataTests(TestCase):
    def test_default_sensor_data_ordering(self):
        test_user = create_user('username', 'password')
        sensor = test_user.sensor_set.create(name = 'test_sensor', device_type = 'device_type')
        
        import datetime
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        before_yesterday = yesterday - datetime.timedelta(days=1)
        
        sensor.sensordata_set.create(created_at= yesterday, data= -1)
        sensor.sensordata_set.create(created_at= today, data= -1)
        sensor.sensordata_set.create(created_at= before_yesterday, data= -1)

        self.assertEqual(SensorData.objects.all()[0].created_at.day, before_yesterday.day)
        self.assertEqual(SensorData.objects.all()[1].created_at.day, yesterday.day)
                
class RestApiTests(APITestCase):
    def test_login(self):
        username = 'teste'
        password = 'password'
        test_user = create_user(username, password)
        data = {'username': username, 'password': password}
        json_data = json.dumps(data)
        response = self.client.post('/datacenter/login.json', data = json_data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data.get('user').get('id'), test_user.id)
        self.assertFalse(data['user']['is_staff'])
        self.assertIsNotNone(data.get('session-id'))
        
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
        
    def test_create_sensor_with_data_type_and_device_type(self):
        username = 'teste'
        password = 'password'
        sensor_name = "unread msg"
        sensor_display_name = "message waiting"
        sensor_data_type = "bool"
        sensor_device_type = "unread msg"
        
        test_user = create_user(username, password)
        login = self.client.login(username = username, password = password)
        sensor_data = {"sensor":{"display_name": sensor_display_name,"pager_type":"","data_type":sensor_data_type,"device_type": sensor_device_type,"name":sensor_name}}
        json_data = json.dumps(sensor_data)
        response = self.client.post('/datacenter/sensors.json', data = json_data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Response status is not 201')
        data = json.loads(response.content)
        
        sensor_id = data.get('sensor').get('id')
        self.assertIsNotNone(sensor_id, 'Sensor id is not present in response')
        sensor = Sensor.objects.get(id=sensor_id)
        self.assertIsNotNone(sensor, 'Sensor with the provided id is not found')
        self.assertEqual(sensor.data_type, sensor_data_type)
        self.assertEqual(sensor.device_type, sensor_device_type)
        
    
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
        
    def test_list_sensors_with_device(self):
        username = 'teste'
        password = 'password'
        test_user = create_user(username, password)
        self.client.login(username = username, password = password)
        sensor_name = 'sensor_test'
        sensor = create_sensor(test_user, sensor_name)
        device_type = 'iPhone Simulator'
        device_uuid = '620A033F-4738-4319-AAC8-0F27B310AA82'
        device = create_device(device_type, device_uuid)
        device.sensor_set.add(sensor)
        
        response = self.client.get('/datacenter/sensors', {})
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'List sensors did not return 200')
        data = json.loads(response.content)
        retrieved_sensor_data = data.get('sensors')[0]
        retrieved_sensor_device_data = retrieved_sensor_data.get('device')
        self.assertIsNotNone(retrieved_sensor_device_data, 'List sensors did not include device information')
        self.assertEqual(retrieved_sensor_device_data.get('uuid'), device_uuid)
        
        
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
        
    def test_register_user_with_profile_fields(self):
        username = 'janjager'
        password = 'password'
        student_id = '060509034'
        institution = 'FEUP'
        user_data = {
            "user": {
                "username": username,
                "email": "jan@test.nl",
                "password": password,
                "student_id": student_id,
                "institution": institution
            }
        }
        json_data = json.dumps(user_data)
        response = self.client.post('/datacenter/users.json', data = json_data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Create user did not return 201')
        created_user = User.objects.get(username=username)
        self.assertEqual(created_user.profile.student_id, student_id)
        self.assertEqual(created_user.profile.institution, institution)
        
    def test_register_existent_user_returns_409(self):
        user_data = {"user":
            {"username":"ei06034@fe.up.pt","email":"ei06034@fe.up.pt","address":"","zipCode":"","name":"Luis","student_id":"student_id","surname":"cruz","password":"fe01ce2a7fbac8fafaed7c982a04e229","country":"PORTUGAL","institution":"feup","mobile":""}
        }
        json_data = json.dumps(user_data)
        response = self.client.post('/datacenter/users.json', data = json_data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Create first user did not return 201')
        response = self.client.post('/datacenter/users.json', data = json_data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT, 'Trying to create already registered user should return HTTP_409_CONFLICT')

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
        
    def test_basic_analytics(self):
        username = 'teste'
        password = 'password'
        test_user = create_superuser(username, password)
        
        response = self.client.get('/datacenter/basic_analytics', {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        login = self.client.login(username = username, password = password)
        response = self.client.get('/datacenter/basic_analytics', {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = json.loads(response.content)
        users_connected = data.get('users_connected')
        self.assertEqual(users_connected, 1)
        
        
    def test_basic_analytics_users_connected(self):
        username = 'teste'
        password = 'password'
        test_user = create_user(username, password)
        login = self.client.login(username = username, password = password)
        response = self.client.get('/datacenter/basic_analytics', {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        set_as_superuser(test_user)        
        response = self.client.get('/datacenter/basic_analytics', {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = json.loads(response.content)
        users_connected = data.get('users_connected')
        self.assertEqual(users_connected, 1)
        
    def test_data_uploaded_per_day(self):
        response = self.client.get('/datacenter/data_uploaded_per_day', {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_users(self):
        username = 'teste'
        password = 'password'
        test_user = create_user(username, password)
        
        response = self.client.get('/datacenter/users', {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        login = self.client.login(username = username, password = password)
        response = self.client.get('/datacenter/users', {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        set_as_superuser(test_user)
        test_user.save()
        response = self.client.get('/datacenter/users', {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_users_show(self):
        username = 'teste'
        password = 'password'  
        test_user = create_user(username, password)
        response = self.client.get('/datacenter/users/'+str(test_user.id), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        login = self.client.login(username = username, password = password)
        response = self.client.get('/datacenter/users/'+str(test_user.id), {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    