from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User
from django.utils import timezone
#from datacenter.serializers import *

# Create your models here.
    
class Sensor(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200, blank=True, null=True)
    device_type = models.CharField(max_length=200, blank=True, null=True)        
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name, 
            'device_type': self.device_type,
            'display_name': self.display_name,
        }
    
class SensorData(models.Model):
    sensor = models.ForeignKey(Sensor)
    created_at = models.DateTimeField(default=timezone.now) #sensor read this calue at this time
    data = JSONField()
