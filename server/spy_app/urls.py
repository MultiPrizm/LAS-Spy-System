from django.urls import path
from spy_app.views import *

urlpatterns = [
    path("history/", sent_browser_history),
    path("report/", send_work_report),
]