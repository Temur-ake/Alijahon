# Generated by Django 5.1.1 on 2024-10-20 04:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0015_alter_order_status_delete_currierprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='courier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='couriers', to=settings.AUTH_USER_MODEL, verbose_name='Mahsulot Yetkazib Beruvchi'),
        ),
    ]