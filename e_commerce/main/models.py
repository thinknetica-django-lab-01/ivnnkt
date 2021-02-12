from django.db import models
from django.contrib.flatpages.models import FlatPage
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import datetime
from apscheduler.schedulers.background import BackgroundScheduler


class NewFlatpage(models.Model):
    flatpage = models.OneToOneField(FlatPage, on_delete=models.CASCADE)
    content = RichTextUploadingField(verbose_name='Контент', default='')

    def __str__(self):
        return self.flatpage.title

    class Meta:
        verbose_name = "Содержание страницы"
        verbose_name_plural = "Содержание страницы"


class Seller(models.Model):
    '''
    Продавцы (возможно производители)
    '''
    name = models.CharField(verbose_name="Название", max_length=250)

    def __str__(self):
        return self.name


class Category(models.Model):
    '''
    Категории товаров в магазине
    '''
    name = models.CharField(verbose_name="Название", max_length=250)
    discription = models.TextField(verbose_name="Описание категории")

    def __str__(self):
        return self.name


class Tag(models.Model):
    '''
    Тэги для поиска товара
    '''
    name = models.CharField(verbose_name="#Тэг", max_length=50, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    '''
    Товар представленный в магазине
    '''
    name = models.CharField(verbose_name="Название", max_length=250)
    discription = models.TextField(verbose_name="Описание товара")
    price = models.IntegerField(verbose_name="Цена")
    in_stock = models.IntegerField(verbose_name="Наличие", blank=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    '''
    Профиль пользователя
    '''
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.IntegerField(verbose_name="Возраст", blank=True, null=True)

    def __str__(self):
        return self.username.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='common users'))


def send_msg_to_new_user(sender, instance, created, **kwargs):
    if created:
        email = User.email
        data = {
            'name': User.username,
        }
        html_content = render_to_string('email_temlates/welcome_messege.html', data)
        msg = EmailMultiAlternatives(
            subject='Welcome messege',
            from_email='from@example.com',
            to = [email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

post_save.connect(send_msg_to_new_user, sender=User)


class Subscriber(models.Model):
    '''
    Подписка на новинки
    '''
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username.username


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


def week_new_product(sender, instance, created, **kwargs):
        sub_list = Subscriber.objects.all()
        email = [user.username.email for user in sub_list]
        week_date = datetime.date.today() - datetime.timedelta(days=7)
        product_list = Product.objects.filter(date__gte=week_date)
        html_content = render_to_string(
            'email_temlates/week_new.html',
            {'product_list': product_list}
        )
        msg = EmailMultiAlternatives(
            subject='New in the site',
            from_email='from@example.com',
            to = email
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


# scheduler = BackgroundScheduler()
# scheduler.add_job(week_new_product, 'interval', day=7)
# scheduler.start()

