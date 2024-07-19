from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    GENDER_CHOICE = [
        ('Male', '남자'),
        ('Female', '여자'),
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=20, null=True, blank=True, unique=True, default="User")  # 기본값 추가
    birth = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, null=True)
    game_score = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
