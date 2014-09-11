from django.shortcuts import render

from datacenter.models import User
from datacenter.serializers import UserSerializer

from rest_framework import mixins
from rest_framework import generics
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
