# Generated by Django 3.1.5 on 2021-01-23 22:55

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newflatpage',
            name='text_block',
        ),
        migrations.AlterField(
            model_name='newflatpage',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='', verbose_name='Контент'),
        ),
    ]
