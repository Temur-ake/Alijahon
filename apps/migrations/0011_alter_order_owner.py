# Generated by Django 5.1.1 on 2024-10-06 09:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0010_product_discount_market'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(blank=True, default='user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Mahsulot Beruvchi'),
        ),
    ]
