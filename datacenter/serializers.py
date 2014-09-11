from rest_framework import serializers
from datacenter.models import User, ActivityLog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'gender', 'date_of_birth')
    
    # pk = serializers.Field();
#     first_name = serializers.CharField(max_length=200)
#     last_name = serializers.CharField(max_length=200)
#     email = serializers.EmailField()
#     gender = serializers.ChoiceField(choices = User.GENDER_CHOICES, required = False)
#     date_of_birth = serializers.DateField(blank=True, required=False)
#
#     def restore_object(self, attrs, instance=None):
#         """
#         Create or update a new snippet instance, given a dictionary
#         of deserialized field values.
#
#         Note that if we don't define this method, then deserializing
#         data will simply return a dictionary of items.
#         """
#         if instance:
#             # Update existing instance
#             instance.first_name = attrs.get('first_name', instance.first_name)
#             instance.last_name = attrs.get('last_name', instance.last_name)
#             instance.email = attrs.get('email', instance.email)
#             instance.gender = attrs.get('gender', instance.gender)
#             instance.date_of_birth = attrs.get('date_of_birth', instance.date_of_birth)
#             return instance
#
#         # Create new instance
#         return User(**attrs)