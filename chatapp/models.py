from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    preferred_tone = models.CharField(max_length=50, default='gentle')

    def __str__(self):
        return self.user.username

