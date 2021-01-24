"""примеры запросов в БД"""

# отфильтровать товары по продавцу
Product.objects.filter(seller__name = 'Sport24')
# найти товар с определенной ценой
Product.objects.get(price=25)
# найти товары относящиеся к категории
Product.objects.filter(category__name = "Бытовая техника")
# показать всех продавцов
Seller.objects.all()
# создание продавца через create
s2 = Seller.objects.create(name="Electronics")
# создание категории через create
c3 = Category.objects.create(
    name = "Гаджеты",
    discription = "В данной категории представленны мобильные телефоны и планшеты"
)
# создание товара через save
p4 = Product(name = "Смартфон", discription = "Модный телефон с супер экраном", price = "500")
p4.seller = s3
p4.category = c3
p4.save()

