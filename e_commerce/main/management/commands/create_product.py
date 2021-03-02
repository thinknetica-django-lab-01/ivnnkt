from django.contrib.auth.models import User
from main.models import Product, Seller, Category
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from random import randint


class Command(BaseCommand):
    help = "Создание товара и юзера(владельца товара)"

    def handle(self, *args, **kwargs):
        user = User.objects.get(username='admin')

        seller = Seller.objects.create(name='test_seller')
        category = Category.objects.create(
            name='test_category',
            discription='test_discr',
        )
        Product.objects.create(
            name='product',
            discription=get_random_string(),
            price=randint(1,100),
            in_stock=1,
            category=category,
            seller=seller,
            owner=user,
        )