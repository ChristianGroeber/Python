from django import forms
from .models import UserLogin, Game


class Login(forms.ModelForm):

    class Meta:
        model = UserLogin
        fields = ('username', 'password')


class NewGame(forms.ModelForm):

    class Meta:
        model = Game
        fields = ('player',)
