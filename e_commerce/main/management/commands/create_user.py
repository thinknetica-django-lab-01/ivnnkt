from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = "Создание случайного пользователя"

    def handle(self, *args, **kwargs):
        name = get_random_string()
        User.objects.create_user(username=name, email=f'{name}@mail.net', password='pass1234')
