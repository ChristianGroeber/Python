from django import forms
from .models import Game


class NewGame(forms.ModelForm):

    class Meta:
        model = Game
        fields = ('player',)
