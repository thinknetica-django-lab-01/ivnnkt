from django.db import models
from django.contrib.flatpages.models import FlatPage
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.postgres.fields import ArrayField


class NewFlatpage(models.Model):
    """Создание плоских страниц из админки."""
    flatpage = models.OneToOneField(FlatPage, on_delete=models.CASCADE)
    content = RichTextUploadingField(verbose_name='Контент', default='')

    def __str__(self):
        return self.flatpage.title

    class Meta:
        verbose_name = "Содержание страницы"
        verbose_name_plural = "Содержание страницы"


class Seller(models.Model):
    """Модель Продавец - название магазина предоставляющего товар.

    Название -- поле CharField, максимальной длинной 250 символов.
    """
    name = models.CharField(verbose_name="Название", max_length=250)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель Категории товаров - служит для отнесения товаров к
    определенной категории, например элетроника, спорттовары,
    товары для дома и т.д.

    Название -- поле CharField, максимальной длинной 250 символов.
    Описание -- поле TextField.
    """
    name = models.CharField(verbose_name="Название", max_length=250)
    discription = models.TextField(verbose_name="Описание категории")

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель Товар - товары представленные в магазине.

    Название -- поле CharField, максимальной длинной 250 символов.
    Описание -- поле TextField, содержит описание товара.
    Цена -- поле IntegerField.
    Наличие на складе -- поле IntegerField, (default  0).
    Продавец -- используется модель Продавец, связь один ко мнгим.
    Категория -- Используется модель Категории товаров,
    связь связь один ко многим.
    Тэг -- используется модель Тэг, связ многие ко многим.
    Владелец -- Используется модель Пользователя, владелец привязыватся к
    товару атоматически приего создании, только владелец и админ могут
    редактировать карточку товара, связ один ко многим.
    Дата -- заполняется автоматически присоздании товара, необходима для
    формирования списка новинок за неделю.
    Счетчик -- счетчик просмотров, (default  0).
    """
    name = models.CharField(verbose_name="Название", max_length=250)
    discription = models.TextField(verbose_name="Описание товара")
    price = models.IntegerField(verbose_name="Цена")
    in_stock = models.IntegerField(verbose_name="Наличие", blank=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )
    tag = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    counter = models.IntegerField(
        verbose_name="Количество просмотров",
        default=0
    )
    published = models.BooleanField(
        default=False,
        verbose_name='Опубликован'
    )

    def __str__(self):
        return self.name


class Profile(models.Model):
    """Модель Профиль пользователя - асширяет стандартную модель User,
    добавляя дату рождения и возраст. Возрст не может быть меньше 18 лет.

    Дата рождения -- поле может быть не заполнено.
    Возраст -- поле может быть не заполнено.
    """
    username = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.IntegerField(verbose_name="Возраст", blank=True, null=True)

    def __str__(self):
        return self.username.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """По сигналу о сохрании нового пользователя автоматически добавляет
    его в группу common users.
    """
    if created:
        instance.groups.add(Group.objects.get(name='common users'))


def send_msg_to_new_user(sender, instance, created, **kwargs):
    """Формирует приветственное сообщение новому пользователю и отправляет
    его по сигналу о создании нового пользователя.

    :param sender: принимает модель User, и извлекает из нее имя пользователя
    и его email.
    формирует письмо с помощью метода render_to_string() из html шаблона и
    пременной data в которую помещает имя пользователя.
    """
    if created:
        email = User.email
        data = {
            'name': User.username,
        }
        html_content = render_to_string(
            'email_temlates/welcome_messege.html',
            data
        )
        msg = EmailMultiAlternatives(
            subject='Welcome messege',
            from_email='from@example.com',
            to=[email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


post_save.connect(send_msg_to_new_user, sender=User)


class Subscriber(models.Model):
    """Модель Подпискчик и используется для отправки новинок недели
    подписавшимся пользователям. Подписаться может только зарегистрированный
    пользователь, email для рассылки береться из модели User.

    Имя пользователя -- используется модель User, связь один ко многим.
    """
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username.username


class UserProduct(models.Model):
    product = models.CharField(max_length=250)
    user = models.CharField(max_length=250)

    class Meta:
        managed = False


# def send_new_product(sender, instance, created, **kwargs):
#     if created:
#         sub_list = Subscriber.objects.all()
#         email = [user.username.email for user in sub_list]
#         html_content = render_to_string('email_temlates/new.html')
#         msg = EmailMultiAlternatives(
#             subject='New in the site',
#             from_email='from@example.com',
#             to = email
#         )
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()
#
# post_save.connect(send_new_product, sender=Product)


# def week_new_product(sender, instance, created, **kwargs):
#         sub_list = Subscriber.objects.all()
#         email = [user.username.email for user in sub_list]
#         week_date = datetime.date.today() - datetime.timedelta(days=7)
#         product_list = Product.objects.filter(date__gte=week_date)
#         html_content = render_to_string(
#             'email_temlates/week_new.html',
#             {'product_list': product_list}
#         )
#         msg = EmailMultiAlternatives(
#             subject='New in the site',
#             from_email='from@example.com',
#             to = email
#         )
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()


# scheduler = BackgroundScheduler()
# scheduler.add_job(week_new_product, 'interval', day=7)
# scheduler.start()
