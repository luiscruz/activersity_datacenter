from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseBadRequest
from django.contrib import auth
from django.contrib.auth.decorators import login_required

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

# Create your views here.

# class UserList(generics.ListCreateAPIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# class ActivityLogList(generics.ListCreateAPIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     queryset = ActivityLog.objects.all()
#     serializer_class = ActivityLogSerializer
#     # def pre_save(self, obj):
#     #     obj.user = self.request.user
#
# class ActivityLogDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     queryset = ActivityLog.objects.all()
#     serializer_class = ActivityLogSerializer
#     # def pre_save(self, obj):
# #         obj.user = self.request.user

#POST
def login(request): 
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            # Redirect to a success page.
            return HttpResponse( status = status.HTTP_200_OK)
        else:
            # Return a 'disabled account' error message
            return HttpResponse( status = status.HTTP_401_UNAUTHORIZED)
    else:
        # Return an 'invalid login' error message.
        return HttpResponse( status = status.HTTP_401_UNAUTHORIZED)
            
    
    

#POST    
def logout(request):
    auth.logout(request)
    return HttpResponse('Logout!')
    
    
class SensorsView(View):
    #list_sensors
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/login/?next=%s' % request.path)
        sensors = request.user.sensor_set.all()
        sensors_list = []
        for sensor in sensors:
            sensors_list.append(sensor.to_dict())
        data = {'sensors': sensors_list}
        return JsonResponse(data)
        
    #create_sensor
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/login/?next=%s' % request.path)
        description = request.POST.get('description')
        display_name = request.POST.get('display_name')
        device_type = request.POST.get('device_type')
        sensor = request.user.sensor_set.create(name = description, display_name = display_name, device_type = device_type)
        return JsonResponse({'sensor':sensor.to_dict()},  status = status.HTTP_201_CREATED)

class SensorsDataView(View):
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
                        created_at = date.fromtimestamp(float(created_at))
                    else:
                        created_at = timezone.now()
                sensor.sensordata_set.create(data = data_item, created_at = created_at)
                
            return HttpResponse('Upload Data!', status = status.HTTP_201_CREATED)
        else:
            return HttpResponseBadRequest()

@login_required
def upload_data_for_multiple_sensors(request, format = None):
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
                        created_at = date.fromtimestamp(float(created_at))
                    else:
                        created_at = timezone.now()
                sensor.sensordata_set.create(data = data_item, created_at = created_at)
                
        return HttpResponse('Upload Data!', status = status.HTTP_201_CREATED)
    else:
        return HttpResponseBadRequest()
    
#POST
def register_user(request, format = None):
    request_data = json.loads(request.body)
    user_data = request_data.get('user')
    if user_data is not None:
        User.objects.create(
            username = user_data.get('username'),
            email = user_data.get('email'),
            first_name = user_data.get('name'),
            password = user_data.get('password')
        )
    return HttpResponse('User registered!', status = status.HTTP_201_CREATED)

