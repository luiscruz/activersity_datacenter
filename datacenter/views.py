from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseBadRequest
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count

from django.contrib.sessions.models import Session

# from datacenter.models import User,ActivityLog
# from datacenter.serializers import UserSerializer, ActivityLogSerializer
from django.views.generic import View

from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status

from rest_framework.renderers import JSONRenderer
from datacenter.serializers import *
from django.core import serializers

from django.core import serializers
import json
from datetime import date
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt


def test(request, format = None):
    return HttpResponse('It is fine ;)')

#POST
@csrf_exempt
def login(request, format = None): 

    request_data = json.loads(request.body)
    
    username = request_data.get('username')
    password = request_data.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            # Redirect to a success page.
            user  = UserWithExtraMethods.objects.get(id = user.id)
            data = {'session_id': request.session.session_key,'session-id': request.session.session_key, 'user': user.to_dict()}
            return JsonResponse(data, status = status.HTTP_200_OK)
        else:
            # Return a 'disabled account' error message
            return HttpResponse( status = status.HTTP_401_UNAUTHORIZED)
    else:
        # Return an 'invalid login' error message.
        return HttpResponse( status = status.HTTP_401_UNAUTHORIZED)
            
    
    

#POST    
def logout(request, format = None):
    auth.logout(request)
    return HttpResponse('Logout!')
    
    
class SensorsView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SensorsView, self).dispatch(*args, **kwargs)
        
    #list_sensors
    def get(self, request, *args, **kwargs):
        # if not request.user.is_authenticated():
        #   return JsonResponse({}, status = status.HTTP_401_UNAUTHORIZED)
        sensors = request.user.sensor_set.all()
        sensors_list = []
        for sensor in sensors:
            sensors_list.append(sensor.to_dict())
        data = {'sensors': sensors_list}
        return JsonResponse(data)
        
    #create_sensor
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse({}, status = status.HTTP_401_UNAUTHORIZED)
        request_data = json.loads(request.body).get('sensor')
        
        name = request_data.get('name')
        display_name = request_data.get('display_name')
        device_type = request_data.get('device_type')
        device = request_data.get('device')
        data_type = request_data.get('data_type')
        
        sensor = request.user.sensor_set.create(name = name, display_name = display_name, device_type = device_type, device = device, data_type = data_type)
        response = JsonResponse({'sensor':sensor.to_dict()},  status = status.HTTP_201_CREATED)
        response['Location'] = 'http://localhost:8000/datacenter/sensors/'+str(sensor.id)
        return response

class SensorsDataView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SensorsDataView, self).dispatch(*args, **kwargs)
    
    #get data from sensor
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/login/?next=%s' % request.path)
        
        pk = kwargs.get('pk')
        sensor = Sensor.objects.get(pk = pk)
        data = SensorDataSetSerializer(sensor).to_dict()
        return JsonResponse(data)
        
    #upload data
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/login/?next=%s' % request.path)
        
        pk = kwargs.get('pk')
        sensor = Sensor.objects.get(pk = pk)        
        request_data = json.loads(request.body).get('data')#request.POST.getlist('data')  
              
        if request_data is not None:
            for data_item in request_data:
                created_at = data_item.get('created_at')
                if created_at is None:
                    created_at = data_item.get('date')
                    if created_at is not None:
                        created_at = datetime.fromtimestamp(float(created_at))
                    else:
                        created_at = timezone.now()
                sensor.sensordata_set.create(data = data_item, created_at = created_at)
                
            return HttpResponse('Upload Data!', status = status.HTTP_201_CREATED)
        else:
            return HttpResponseBadRequest()

@csrf_exempt
@login_required
def upload_data_for_multiple_sensors(request, format = None):
    print 'upload_data_for_multiple_sensors'
    request_data = json.loads(request.body).get('sensors')#request.POST.getlist('data')
    if request_data is not None:
        for sensor_data in request_data:
            sensor_id = sensor_data.get('sensor_id')
            sensor = Sensor.objects.get(id = sensor_id)
            for data_item in sensor_data.get('data'):
                created_at = data_item.get('created_at')
                if created_at is None:
                    created_at = data_item.get('date')
                    if created_at is not None:
                        created_at = datetime.fromtimestamp(float(created_at))
                    else:
                        created_at = timezone.now()
                sensor.sensordata_set.create(data = data_item, created_at = created_at)
                
        return HttpResponse('Upload Data!', status = status.HTTP_201_CREATED)
    else:
        return HttpResponseBadRequest()
    

@csrf_exempt 
def sensor_device(request, pk, format = None):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        device_data = request_data.get('device')
        sensor = Sensor.objects.get(pk = pk)
        device_type = device_data.get('type')
        device_uuid = device_data.get('uuid')
        device = sensor.set_device(device_type = device_type, uuid = device_uuid)
        return JsonResponse({'device': device.to_dict()}, status=status.HTTP_201_CREATED)
    else:
        print '***********'
        print "sensor device"
        print response
        print response.body
        print '***********'
        
        
############## Users ##############
#POST
@csrf_exempt
def users(request, format = None):
    if request.method == 'GET':
        user = request.user
        if not (user.is_authenticated() and user.is_staff):
            return JsonResponse({}, status = status.HTTP_401_UNAUTHORIZED)
        users = User.objects.all().values()
        return JsonResponse({"users": list(users)})
        
    elif request.method == 'POST':
        request_data = json.loads(request.body)
        user_data = request_data.get('user')
        if user_data is not None:
            username = user_data.get('username')
            if User.objects.filter(username=username).exists():
                return HttpResponse('User already registered!', status = status.HTTP_409_CONFLICT)
            user = User.objects.create_user(
                username = username,
                email = user_data.get('email'),
                first_name = user_data.get('name') or '',
                last_name = user_data.get('surname') or '',
                password = user_data.get('password')
            )
            userProfile = Profile.objects.create(
                user=user,
                institution = user_data.get('institution') or '',
                student_id = user_data.get('student_id') or ''
            )
        return HttpResponse('User registered!', status = status.HTTP_201_CREATED)
        
def users_show(request, user_id, format = None):
    if request.method == 'GET':
        user = UserWithExtraMethods.objects.get(id=user_id)
        if not (request.user.is_authenticated() and request.user.is_staff or user == request.user):
            return JsonResponse({}, status = status.HTTP_401_UNAUTHORIZED)
        return JsonResponse({"user": user.to_dict(True)})

###################################        
        
        
############ Analytics ############
def get_users_connected():###DEAD CODE - HELPER
    # Query all non-expired sessions
    sessions = Session.objects.filter(expire_date__gte=datetime.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))
    
    # Query all logged in users based on id list
    return User.objects.filter(id__in=uid_list)
    
def get_users_connected_count(): ### - HELPER
    # Query all non-expired sessions
    sessions = Session.objects.filter(expire_date__gte=datetime.now())
    return sessions.count()

def basic_analytics(request, format = None):
    if not (request.user.is_authenticated() and request.user.is_staff):
        return JsonResponse({}, status = status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        import numpy
        sensors_count = Sensor.objects.count()
        users_count = User.objects.count()
        sensors_per_user = numpy.float64(sensors_count)/users_count
        devices_count = Device.objects.count()
        devices_per_user = numpy.float64(devices_count)/users_count
        response_data = {
            'sensors_count': sensors_count,
            'users_count': users_count,
            'sensors_per_user': sensors_per_user,
            'users_connected': get_users_connected().count(),
            'devices_count': devices_count,
            'devices_connected': -1,
            'devices_per_user': devices_per_user,
            'devices_ios': -1,
            'devices_android': -1
        }
        return JsonResponse(response_data)

def data_uploaded_per_day(request, format = None):
    if request.method == 'GET':
        array = SensorData.objects.extra({'created':"date(created_at)"}).values('created_at').annotate(created_count=Count('id')) 
        return JsonResponse({"data_uploaded_per_day": list(array)})
        

###################################
