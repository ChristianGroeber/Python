from django import forms

from .models import Check

class PostForm(forms.ModelForm):

    class Meta:
        model = Check
        fields = ('name', 'age', 'love_for_beer')
