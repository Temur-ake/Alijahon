# Generated by Django 5.1.1 on 2024-11-02 09:15

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0020_alter_order_courier_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Mahsulot haqida'),
        ),
    ]
