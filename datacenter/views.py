from django.shortcuts import render

from datacenter.models import User, ActivityLog
from datacenter.serializers import UserSerializer, ActivityLogSerializer

from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
# Create your views here.

class UserList(generics.ListCreateAPIView):
    """
    List all snippets, or create a new snippet.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
        
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ActivityLogList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    # def pre_save(self, obj):
    #     obj.user = self.request.user
    
class ActivityLogDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    # def pre_save(self, obj):
#         obj.user = self.request.user