from django import forms
from .models import Idea

class newBoxForm(forms.Form):
    box_name = forms.CharField(label='Box name', max_length=100)

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = '__all__'