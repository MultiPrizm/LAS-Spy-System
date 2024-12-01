from django import forms
from authorization.models import WorkStation

class AddWorkstationForm(forms.ModelForm):
    class Meta:
        model = WorkStation
        fields = ['name']