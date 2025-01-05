from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.urls import path
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from adminpanel.models import *
from authorization.models import AuthToken, WorkStation
from spy_app.models import *

class BasicAdmin(admin.AdminSite):
    site_header = "Admin Panel"
    site_title = "Admin Panel"
    index_title = "Welcome to the Admin Panel"

    def has_permission(self, request: WSGIRequest) -> bool:
        return request.user.is_superuser

    def index(self, request, extra_context=None):

        extra_context = extra_context or {}
        extra_context['custom_menu'] = [
            {"name": "Root panel", "url": "/admin/root/"},
            {"name": "Security panel", "url": "/admin/security/"},
            {"name": "Work panel", "url": "/admin/work/"},
        ]

        return super().index(request, extra_context=extra_context)

class RootAdmin(admin.AdminSite):
    site_header = "Root Admin Panel"
    site_title = "Root Admin Panel"
    index_title = "Welcome to the Root Admin Panel"

    def has_permission(self, request: WSGIRequest) -> bool:
        return request.user.has_perm(request.user.has_perm("security_admin"))

    def index(self, request, extra_context=None):

        extra_context = extra_context or {}
        extra_context['custom_menu'] = [
            {"name": "Return to home", "url": "/admin"},
        ]

        return super().index(request, extra_context=extra_context)

class SecurityAdmin(admin.AdminSite):
    site_header = "Security Admin Panel"
    site_title = "Security Admin Panel"
    index_title = "Welcome to the Security Admin Panel"

    def has_permission(self, request: WSGIRequest) -> bool:
        return request.user.has_perm(request.user.has_perm("work_admin"))
    
    def index(self, request, extra_context=None):

        extra_context = extra_context or {}
        extra_context['custom_menu'] = [
            {"name": "Return to home", "url": "/admin"},
        ]

        return super().index(request, extra_context=extra_context)

class WorkAdmin(admin.AdminSite):
    site_header = "Work Admin Panel"
    site_title = "Work Admin Panel"
    index_title = "Welcome to the Work Admin Panel"

    def has_permission(self, request: WSGIRequest) -> bool:
        return request.user.has_perm(request.user.has_perm("security_admin"))

    def index(self, request, extra_context=None):

        extra_context = extra_context or {}
        extra_context['custom_menu'] = [
            {"name": "Return to home", "url": "/admin"},
        ]

        return super().index(request, extra_context=extra_context)

basic_panel = BasicAdmin(name = "basic")

root_admin = RootAdmin(name = "root")
root_admin.register(User, UserModel)

security_admin = SecurityAdmin(name = "security")
security_admin.register(AuthToken, AuthJWT)
security_admin.register(WorkStation, WorkStationAdminModel)
security_admin.register(Worker, WorkerAdminModel)

work_admin = WorkAdmin(name = "work")
work_admin.register(DailyWorkReport, AdminDailyWorkReportModel)
work_admin.register(BrowserHistoryItem, AdminBrowserHistoryItem)
work_admin.register(Worker, WorkerProtectAdminModel)