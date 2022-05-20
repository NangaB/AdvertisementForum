from django import forms
from .models import Advertisement

class AdForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['company', 'adress', 'email']
