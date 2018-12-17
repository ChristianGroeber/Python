from django import forms
from .models import Kommentar


class Kommentar(forms.ModelForm):

    class Meta:
        model = Kommentar
        fields = ('titel', 'text')
