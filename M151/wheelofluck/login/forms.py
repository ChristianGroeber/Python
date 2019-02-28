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


class Konsonant(forms.ModelForm):

    class Meta:
        model = Game
        fields = ('konsonant',)


class Solve(forms.Form):
    Question = forms.CharField(max_length=200)


class Setzen(forms.Form):
    betrag = forms.CharField(max_length=100)
