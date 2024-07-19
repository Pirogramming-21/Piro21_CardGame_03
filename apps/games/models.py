from django.db import models
from apps.users.models import User

# Create your models here.
class Game(models.Model):
    STATUS_CHOICES = [
        ('PENDING', '진행중'),
        ('COMPLETED', '완료'),
    ]
    WIN_CONDITION_CHOICES = [
        ('HIGHER', '큰 숫자가 이김'),
        ('LOWER', '작은 숫자가 이김'),
    ]

    player1 = models.ForeignKey(User, related_name='games_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='games_as_player2', on_delete=models.CASCADE)
    player1_card = models.IntegerField(null=True)
    player2_card = models.IntegerField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    result = models.CharField(max_length=10, null=True)
    win_condition = models.CharField(max_length=10, choices=WIN_CONDITION_CHOICES, default='HIGHER')
    created_at = models.DateTimeField(auto_now_add=True)