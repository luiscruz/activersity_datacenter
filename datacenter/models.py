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
    data_type = models.CharField(max_length=200, blank=True, null=True)     
    
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
        instance_dict = {
            'id': self.id,
            'name': self.name, 
            'device_type': self.device_type,
            'display_name': self.display_name,
             "type": "0",
             "data_type_id": "35445",
             "pager_type": "email",
             "use_data_storage": "1",
             "data_type": self.data_type,
             "data_structure":  {"x-axis":"float","y-axis":"float","z-axis":"float"}
        }
        if self.device is not None:
            instance_dict['device'] = self.device.to_dict();
        return instance_dict
    
class SensorData(models.Model):
    sensor = models.ForeignKey(Sensor)
    created_at = models.DateTimeField(default=timezone.now) #sensor read this value at this time
    data = JSONField()
    
    class Meta:
        ordering = ['created_at']
    
# Customize User model
class UserWithExtraMethods(User):
    def to_dict(self, includeAnalytics = None):
        instance_dict = {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            'is_staff': self.is_staff,
            "sensors": list(self.sensor_set.values()),
        }
        if(includeAnalytics):
            instance_dict['analytics'] = self.analytics()
        return instance_dict
        pass

    def data_from_sensor_with_type(self, sensor_device_type):
        return SensorData.objects.filter(sensor__user_id = self.id).filter(sensor__device_type = sensor_device_type)

    def noise_timeline(self):
        sensor_data = self.data_from_sensor_with_type('noise_sensor')
        return list(sensor_data.values('created_at', 'data'))
        
    def position_timeline(self):
        sensor_data = self.data_from_sensor_with_type('position')
        return list(sensor_data.values('created_at', 'data'))
        
    def screen_activity_timeline(self):
        sensor_data = self.data_from_sensor_with_type('screen activity')
        return list(sensor_data.values('created_at', 'data'))
        
    def accelerometer_timeline(self):
        sensor_data = SensorData.objects.filter(sensor__user_id = self.id).filter(sensor__name = 'accelerometer')
        return list(sensor_data.values('created_at', 'data'))
        
    def devices_count(self):
        return self.sensor_set.distinct('device').count()

    def analytics(self):
        return {
            "devices_count": self.devices_count(),
            "sensors_count": self.sensor_set.count(),
            "noise_timeline": self.noise_timeline(),
            "position_timeline": self.position_timeline(),
            "screen_activity_timeline": self.screen_activity_timeline(),
            "accelerometer_timeline": self.accelerometer_timeline(),
        }
        pass

    class Meta:
        proxy=True

# Profile - extra data for user
class Profile(models.Model):
    user = models.OneToOneField(User)
    institution = models.CharField(max_length=200)
    student_id = models.CharField(max_length=200)
    
