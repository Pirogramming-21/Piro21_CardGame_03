from django import forms
from apps.users.models import User
from .models import Game
import random

class GameForm(forms.ModelForm):
    opponent = forms.ModelChoiceField(queryset=User.objects.all(), label="상대 유저 선택")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        random_numbers = kwargs.pop('random_numbers', [])
        super().__init__(*args, **kwargs)
        if self.request:
            self.fields['opponent'].queryset = User.objects.exclude(id=self.request.user.id)
        if random_numbers:
            self.fields['player1_card'].choices = [(num, num) for num in random_numbers]

    class Meta:
        model = Game
        fields = ['opponent', 'player1_card']