from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = "Создание случайного пользователя"

    def add_arguments(self, parser):
        parser.add_argument('-n', '--name', type=str, help='username пользователя', )

        parser.add_argument('-p', '--password', type=str, help='пароль пользователя', )

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        password = kwargs['password']

        if name:
            username = name
        else:
            username = get_random_string()

        if password:
            user_password = password
        else:
            user_password = 'default'

        User.objects.create_user(username=username, email=f'{username}@mail.net', password=user_password)
        self.stdout.write(u'Пользователь успешно создан, login:"%s"!' % (username))
