from typing import Any
from django.core.management import BaseCommand
from users.models import User

class Command(BaseCommand):
    """Команда для создания суперпользователя"""
    def handle(self, *args: Any, **options: Any) -> str | None:
        admin = User.objects.filter(email="admin@mail.ru")
        if not admin.exists():
            admin = User.objects.create(
                email="admin@mail.ru",
                first_name="admin",
                last_name="admin",
                is_staff=True,
                is_superuser=True,
                is_active = True,
            )
            admin.set_password("admin")
            admin.save()
