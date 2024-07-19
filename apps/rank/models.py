from django.db import models
from apps.users.models import User

# Create your models here.
class Rank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

