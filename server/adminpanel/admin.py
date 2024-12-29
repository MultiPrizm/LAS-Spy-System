from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.urls import path
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from adminpanel.models import *
from authorization.models import AuthToken, WorkStation

class BasicAdmin(admin.AdminSite):
    site_header = "Admin Panel"
    site_title = "Admin Panel"
    index_title = "Welcome to the Admin Panel"

    def index(self, request, extra_context=None):

        extra_context = extra_context or {}
        extra_context['custom_menu'] = [
            {"name": "Root panel", "url": "/admin/root/"},
            {"name": "Security panel", "url": "/admin/security/"},
        ]

        return super().index(request, extra_context=extra_context)

class RootAdmin(admin.AdminSite):
    site_header = "Root Admin Panel"
    site_title = "Root Admin Panel"
    index_title = "Welcome to the Root Admin Panel"

    def index(self, request, extra_context=None):

        extra_context = extra_context or {}
        extra_context['custom_menu'] = [
            {"name": "Custom HTML Page", "url": "/admin/root/custom-page/"},
        ]

        return super().index(request, extra_context=extra_context)
    
    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path('custom-page/', self.admin_view(self.custom_html_page), name="custom_html_page"),
        ]

        return custom_urls + urls

    def custom_html_page(self, request):

        context = {
            'title': 'Custom HTML Page',
            'content': '<h1>Welcome to the Custom HTML Page</h1><p>This is some custom HTML content.</p>',
        }

        return TemplateResponse(request, "admin/custom_page.html", context)

class SecurityAdmin(admin.AdminSite):
    site_header = "Security Admin Panel"
    site_title = "Security Admin Panel"
    index_title = "Welcome to the Security Admin Panel"

    def has_permission(self, request: WSGIRequest) -> bool:
        return request.user.has_perm(request.user.has_perm("security_admin"))

basic_panel = BasicAdmin(name = "basic")

root_admin = RootAdmin(name = "root")
root_admin.register(User, UserModel)

security_admin = SecurityAdmin(name = "security")
security_admin.register(AuthToken, AuthJWT)
security_admin.register(WorkStation, WorkStationAdminModel)