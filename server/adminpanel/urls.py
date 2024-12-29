from django.urls import path
from adminpanel.admin import *

urlpatterns = [
    path("security/", security_admin.urls),
    path("root/", root_admin.urls),
    path("", basic_panel.urls)
]