from django import forms
from apps.users.models import User
from .models import Game

class GameForm(forms.ModelForm):
    opponent = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="상대 유저 선택"
    )

    player1_card = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        random_numbers = kwargs.pop('random_numbers', [])
        super().__init__(*args, **kwargs)
        if self.request:
            self.fields['opponent'].queryset = User.objects.exclude(id=self.request.user.id)
        if random_numbers:
            self.fields['player1_card'].choices = [(num, num) for num in random_numbers]

        self.fields['opponent'].label_from_instance = lambda obj: obj.nickname

    class Meta:
        model = Game
        fields = ['opponent', 'player1_card']