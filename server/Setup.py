import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')  # Вказати шлях до налаштувань проєкту

import django
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

try:
    if len(User.objects.filter(username="admin")) == 0:

        user = User(username = "admin", password = make_password("admin"), is_superuser = True, is_staff = 1)
        user.save()

except Exception as e:
    print(f"Сталася помилка: {e}")