from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from .models import *


class NewFlatpageInline(admin.StackedInline):
    model = NewFlatpage
    verbose_name = "Содержание"


class FlatPageNewAdmin(FlatPageAdmin):
    inlines = [NewFlatpageInline]
    fieldsets = (
        (None, {'fields': ('url', 'title', 'sites')}),
        ('Advanced options', {
            'fields': ('template_name',),
        }),
    )
    list_display = ('url', 'title')
    list_filter = ('sites', 'registration_required')
    search_fields = ('url', 'title')


def complete_product(ModelAdmin, reguest, queryset):
    queryset.update(published=True)


complete_product.short_description = 'Опубликовать товары'


def archive_product(ModelAdmin, reguest, queryset):
    queryset.update(published=False)


archive_product.short_description = 'Архивировать товары'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Товары"""

    list_display = ('id', 'name', 'seller', 'owner', 'published',)
    list_display_links = ('name',)
    list_filter = ('seller', 'date', 'tag',)
    actions = [
        complete_product,
        archive_product,
    ]


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageNewAdmin)
admin.site.register(Seller)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Subscriber)
