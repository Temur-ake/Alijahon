# Generated by Django 5.1.1 on 2024-09-29 15:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_product_payment_referral'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='stream',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='apps.stream'),
        ),
    ]
