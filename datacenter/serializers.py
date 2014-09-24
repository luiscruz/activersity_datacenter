from rest_framework import serializers
from datacenter.models import Sensor

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
        
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('id', 'name','display_name')
    
    def to_json(self):
        return {'sensor': self.data}
        