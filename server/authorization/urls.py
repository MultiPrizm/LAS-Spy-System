from django.urls import path
from authorization.views import *

urlpatterns = [
    path("", load_users)
]