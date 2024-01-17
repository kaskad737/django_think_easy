from typing import Any
from django.core.management import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        if User.objects.count() == 0:
            User.objects.create_superuser(
                username='admin',
                password='admin'
                )
            print('Creating account for admin')
        else:
            print(
                'Admin accounts can only be initialized if no Accounts exist'
                )
