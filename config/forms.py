from django import forms
from .models import Config

class ConfigForm(forms.ModelForm):
    class Meta:
        model = Config
        fields = '__all__'