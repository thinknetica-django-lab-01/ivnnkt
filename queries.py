"""примеры запросов в БД"""

# отфильтровать товары по продавцу
Product.objects.filter(seller__name = 'Sport24')
# найти товар с определенной ценой
Product.objects.get(price=25)
# найти товары относящиеся к категории
Product.objects.filter(category__name = "Бытовая техника")
# показать всех продавцов
Seller.objects.all()
