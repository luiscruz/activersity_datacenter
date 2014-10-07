from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# Create your models here.


class Device(models.Model):
    device_type = models.CharField(max_length=200)
    uuid = models.CharField(max_length=200)
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.device_type,
            'uuid': self.uuid
            }

class Sensor(models.Model):
    user = models.ForeignKey(User)
    device = models.ForeignKey(Device, null=True)
    name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200, blank=True, null=True)
    device_type = models.CharField(max_length=200, blank=True, null=True)        
    
    def set_device(self, **kwargs):
        device_type = kwargs.get('device_type')
        uuid = kwargs.get('uuid')
        try:
            device, created = Device.objects.get_or_create(device_type = device_type, uuid = uuid)
            self.device = device
            self.save()
            return device
        except MultipleObjectsReturned:
            #some error ocured :( ignore?
            print 'multiple objects'
            return None
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name, 
            'device_type': self.device_type,
            'display_name': self.display_name,
             "type": "0",
             "data_type_id": "35445",
             "pager_type": "email",
             "use_data_storage": "1",
             "data_type": "json",
             "data_structure":  {"x-axis":"float","y-axis":"float","z-axis":"float"}
        }
    
class SensorData(models.Model):
    sensor = models.ForeignKey(Sensor)
    created_at = models.DateTimeField(default=timezone.now) #sensor read this value at this time
    data = JSONField()
