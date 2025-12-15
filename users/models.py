from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField (
        unique = True,
        error_messages = {
            'unique': 'A user with this email already exits.'
        })
    username = models.CharField(
        max_length = 255,
        unique = True,
        error_messages ={
            'unique': 'A user with this username already exists.'
        })
    profile_image = models.URLField (blank = True, null = True) 
    connections = models.ManyToManyField('self', symmetrical = True, blank = True)
    