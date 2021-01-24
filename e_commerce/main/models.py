from django.db import models

# Create your models here.

from django.contrib.flatpages.models import FlatPage
from ckeditor_uploader.fields import RichTextUploadingField


class NewFlatpage(models.Model):
    flatpage = models.OneToOneField(FlatPage, on_delete=models.CASCADE)
    content = RichTextUploadingField(verbose_name='Контент', default='')

    def __str__(self):
        return self.flatpage.title

    class Meta:
        verbose_name = "Содержание страницы"
        verbose_name_plural = "Содержание страницы"



