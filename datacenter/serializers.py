from rest_framework import serializers
from datacenter.models import *

# class UserSerializer(serializers.ModelSerializer):
#     activitylog_set = serializers.PrimaryKeyRelatedField(many=True)
#     class Meta:
#         model = User
#         fields = ('id', 'first_name', 'last_name', 'email', 'gender', 'date_of_birth', 'activitylog_set')
    
# class ActivityLogSerializer(serializers.ModelSerializer):
#     user = serializers.Field(source='user.id')
#     class Meta:
#         model = ActivityLog
#         fields = ('id', 'data', 'created_at', 'user')
        
class SensorDataSerializer(serializers.ModelSerializer):
    class Meta: 
        model = SensorData
        fields = ('created_at', 'data')
        
class SensorDataSetSerializer(serializers.ModelSerializer):
    data = SensorDataSerializer(many = True, source='sensordata_set')
    class Meta:
        model = Sensor
        fields = ['data']
        
    def to_dict(self):
        return self.data
        