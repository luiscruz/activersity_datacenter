from django.db import models
from jsonfield import JSONField

# Create your models here.

class User(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    gender = models.CharField(max_length=1, choices = GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    def add_activitylog(self, data):
        self.activitylog_set.create(created_at = data['created_at'], data = data)
        
class ActivityLog(models.Model):
    user = models.ForeignKey(User)
    created_at = models.DateTimeField()
    #data = models.TextField(max_length=200)
    data = JSONField()
    
    


