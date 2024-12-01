from django.urls import path
from authorization.views import login
from authorization.admin import admin_site

urlpatterns = [
    path("login/", login),
    path("admin/", admin_site.urls)
]