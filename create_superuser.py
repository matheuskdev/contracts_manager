import os

import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin@example.com", "admin123")
