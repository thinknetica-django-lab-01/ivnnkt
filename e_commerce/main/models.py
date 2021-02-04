from django.db import models
from django.contrib.flatpages.models import FlatPage
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User


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

    def __str__(self):
        return self.name


class Profile(models.Model):
    '''
    Профиль пользователя
    '''
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.IntegerField(verbose_name="Возраст", blank=True, null=True)

    def __str__(self):
        return self.username.username