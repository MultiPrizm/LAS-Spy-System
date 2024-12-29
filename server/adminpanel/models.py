from django.db import models
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.forms import ModelForm
from django.http import HttpRequest
from server.settings import JWT_KEY
from adminpanel.forms import AuthTokenAdminForm
import jwt

class SecurityAdminPermission(models.Model):
    class Meta:
        permissions = [
            ("security_admin", "Can access Security Admin Panel")
        ]

class UserModel(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name")
    search_fields = ("username", "email")
    list_filter = ("is_active", "is_staff")
    exclude = ("last_login", "is_superuser", "date_joined")
    filter_horizontal = ('groups', 'user_permissions')

    def get_changeform_initial_data(self, request):
        return {
            'password': ''
        }

    def save_model(self, request, obj, form, change):
        if "password" in form.changed_data:
            obj.password = make_password(obj.password)
    
        super().save_model(request, obj, form, change)

class AuthJWT(admin.ModelAdmin):
    fields = ("station", "active", "jwt", "description")
    list_display = ("station", "description", "active")
    readonly_fields = ("jwt",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        if 'station' in form.base_fields:
            if obj:
                form.base_fields['station'].widget.attrs['disabled'] = True  # Задаємо атрибут readonly
                print(1)
        
        return form

    def save_model(self, request, obj, form, change):

        data = {
            "station": str(obj.station.id),
            "id": str(obj.id)
        }

        obj.jwt = jwt.encode(data, 'your_jwt_secret', algorithm="HS256")

        return super().save_model(request, obj, form, change)
    
class WorkStationAdminModel(admin.ModelAdmin):
    fields = ("name", "description")