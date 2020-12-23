from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    is_teacher = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    