from django.urls import path
from authorization.views import login

urlpatterns = [
    path("login/", login)
]