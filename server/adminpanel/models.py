from django.db import models
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.forms import ModelForm
from django.http import HttpRequest
from django.core.files.uploadedfile import InMemoryUploadedFile
from server.settings import JWT_KEY
from PIL import Image
from io import BytesIO
import jwt, numpy, json

class SecurityAdminPermission(models.Model):
    class Meta:
        permissions = [
            ("security_admin", "Can access Security Admin Panel"),
            ("work_admin", "Can access Work Admin Panel"),
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
        
        return form

    def save_model(self, request, obj, form, change):

        data = {
            "station": str(obj.station.id),
            "id": str(obj.id)
        }

        obj.jwt = jwt.encode(data, JWT_KEY, algorithm="HS256")

        return super().save_model(request, obj, form, change)
    
class WorkStationAdminModel(admin.ModelAdmin):
    fields = ("name", "description")

class WorkerAdminModel(admin.ModelAdmin):
    exclude = ("face_hash",)
    readonly_fields = ("id",)
    list_display = ("first_name", "last_name", "station")
    search_fields = ("first_name", "station__id", "gmail")

    def save_model(self, request, obj, form, change):
        if "face_image" in form.changed_data:
            image = Image.open(BytesIO(obj.face_image.read())) 

            image_array = numpy.array(image)


            if image_array.size > 10000:

                image_array = image_array[:100, :100]

            obj.face_hash = json.dumps(image_array.tolist()).encode()

        obj.face_image = None

        return super().save_model(request, obj, form, change)

class AdminDailyWorkReportModel(admin.ModelAdmin):
    readonly_fields = ("worker", "date", "start_time", "finish_time", "additional", "common_break_time", "common_work_time", "work_efficiency")
    exclude = ("id",)
    list_display = ("worker", "date")
    list_filter = ("worker", "date")
    search_fields = ("worker__id",)

class AdminBrowserHistoryItem(admin.ModelAdmin):
    readonly_fields = ("id", "profile", "title", "url", "time", "date")
    list_filter = ("worker", "date")
    list_display = ("worker",  "title", "url")
    search_fields = ("worker__id",)

class WorkerProtectAdminModel(admin.ModelAdmin):
    readonly_fields = ("id", "first_name", "last_name", "gmail", "station", "work_time")
    exclude = ("face_image", "face_hash")
    search_fields = ("first_name", "station__id", "gmail")

    def has_change_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False