from django.contrib import admin
from django.urls import path
from authorization.views import add_work_station_model
from authorization.admin_models import AddWorkStation
from authorization.models import WorkStation

class SecurityAdmin(admin.AdminSite):
    site_header = "Security Admin Panel"
    site_title = "Security Admin Panel"
    index_title = "Welcome to Security Admin Panel"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add-my-model/', self.admin_view(add_work_station_model), name="add_my_model"),
        ]
        return custom_urls + urls

admin_site = SecurityAdmin(name="myadmin")

admin_site.register(WorkStation, AddWorkStation)
