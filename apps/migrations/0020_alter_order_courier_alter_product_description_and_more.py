# Generated by Django 5.1.1 on 2024-11-02 08:51

import django.db.models.deletion
import django_ckeditor_5.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0019_remove_orderproxycanceled_order_ptr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='courier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='couriers', to=settings.AUTH_USER_MODEL, verbose_name='Mahsulot Yetkazib Beruvchi'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(max_length=255, verbose_name='Mahsulot haqida'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(verbose_name='Mahsulot narxi'),
        ),
    ]