from django.test import TestCase, RequestFactory
from .models import Product, Seller, Tag, Category
from django.contrib.auth.models import User, Group
from .views import ProductListView,\
    ProductDetailView,\
    ProductCreateView,\
    ProductUpdate


class ProductViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.group = Group.objects.create(name='common users')
        self.seller_group = Group.objects.create(name='sellers')
        self.user = User.objects.create(
            username='User',
            email='user@mail.net',
            password='12345',
        )
        self.seller_user = User.objects.create(
            username='Test_seller',
            email='seller@mail.net',
            password='12345',
        )
        self.seller = Seller.objects.create(name='test_seller')
        self.category = Category.objects.create(
            name='test_category',
            discription='test_discr',
        )
        self.tag = Tag.objects.create(name='#')
        self.product = Product.objects.create(
            name='product',
            discription='product_discription',
            price=10,
            in_stock=1,
            category=self.category,
            seller=self.seller,
            owner=self.seller_user,
            )

    def test_view_uses_correct_template(self):
        resp = self.client.get('/goods/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main/product_list.html')

    def test_view_url(self):
        product_id = self.product.id
        resp = self.client.get('/goods/%s/' % product_id)
        self.assertEqual(resp.status_code, 200)

    def test_product_list_view(self):
        request = self.factory.get('/goods/')
        response = ProductListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        request = self.factory.get('/goods/<int:pk>/')
        response = ProductDetailView.as_view()(request, pk=1)
        self.assertEqual(self.product.pk, 1)
        self.assertEqual(response.status_code, 200)

    def test_product_create_view(self):
        request = self.factory.get('/goods/add/')
        request.user = self.seller_user
        request.user.groups.add(self.seller_group)
        response = ProductCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_product_update_view(self):
        request = self.factory.get('/goods/<int:pk>/edit/')
        request.user = self.seller_user
        request.user.groups.add(self.seller_group)
        response = ProductUpdate.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_product_update_user_is_not_owner(self):
        request = self.factory.get('/goods/<int:pk>/edit/')
        request.user = self.user
        request.user.groups.add(self.seller_group)
        self.assertNotEqual(self.product.owner, request.user)
