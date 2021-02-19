from django.test import TestCase
from .models import Product, Seller, Tag, Category
from django.contrib.auth.models import User


class ProductListViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='User',
            email='user@mail.net',
            password='12345',
        )
        self.seller = Seller.objects.create(name='test_seller')
        self.category = Category.objects.create(
            name='test_category',
            discription='test_discr',
        )
        self.tag = Tag.objects.create(name='#')
        self.product = Product.objects.create(
            name='Goods %s' % product_num,
            discription='Discription goos %s' % product_num,
            price=product_num,
            in_stock=1,
            category=self.category,
            seller=self.seller,
            tag=self.tag,
            owner=self.user,
            )

    def test_view_url(self):
        resp = self.client.get('/goods/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_by_name(self):
        resp = self.client.get(reverse('goods'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('goods'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'main/product_list.html')

    # def test_pagination_is_two(self):
    #     resp = self.client.get(reverse('goods'))
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertTrue('is_paginated' in resp.context)
    #     self.assertTrue(resp.context['is_paginated'] == True)
    #     self.assertTrue(len(resp.context['product_list']) == 2)
    #
    # def test_lists_all_products(self):
    #     resp = self.client.get(reverse('goods') + '?page=2')
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertTrue('is_paginated' in resp.context)
    #     self.assertTrue(resp.context['is_paginated'] == True)
    #     self.assertTrue(len(resp.context['product_list']) == 1)