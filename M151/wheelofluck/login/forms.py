from django import forms
from .models import UserLogin


class Login(forms.ModelForm):

    class Meta:
        model = UserLogin
        fields = ('username', 'password')
