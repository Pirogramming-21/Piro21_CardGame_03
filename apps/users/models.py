from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    GENDER_CHOICE = [
        ('Male', '남자'),
        ('Female', '여자'),
    ]
    username = models.CharField(max_length=10, unique=True, null=True)
    email = models.EmailField( unique=True)
    nickname = models.CharField(max_length=20, null = True, unique=True)
    birth = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, null=True)
