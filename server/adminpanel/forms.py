from django import forms
from django.contrib import admin
from authorization.models import AuthToken

class AuthTokenAdminForm(forms.ModelForm):
    class Meta:
        model = AuthToken
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:

            self.fields['station'].widget = forms.HiddenInput()
        else:

            self.fields['station'].widget = forms.Select()