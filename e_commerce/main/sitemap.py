from django.contrib.sitemaps import Sitemap
from .models import Product
from django.urls import reverse


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Product.objects.filter(published=True)

    def location(self, item):
        return reverse('detail_goods', kwargs={'pk': item.id})
