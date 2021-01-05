from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_teacher = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'profile_id': self.id})

# Default for CharField
class Lesson(models.Model):
    date = models.DateTimeField(default=timezone.now)
    lesson = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=250, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
  

