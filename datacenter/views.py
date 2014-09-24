from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import auth
from django.contrib.auth import authenticate

# from datacenter.models import User,ActivityLog
# from datacenter.serializers import UserSerializer, ActivityLogSerializer
from django.views.generic import View

from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
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
    user = authenticate(username=username, password=password)
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

#POST    
class SensorsDataView(View):

    #get data from sensor
    def get(self, request, *args, **kwargs):
        return HttpResponse('Get data!')
        
    #upload data
    def post(self, request, *args, **kwargs):
        return HttpResponse('Upload Data!', status = status.HTTP_201_CREATED)
        

#POST
def create_sensor(request, format = None):
    return HttpResponse('Create Sensor!', status = status.HTTP_201_CREATED)
    
#POST
def register_user(request):
    return HttpResponse('Register User!')