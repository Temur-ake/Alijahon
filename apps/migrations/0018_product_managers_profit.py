# Generated by Django 5.1.1 on 2024-10-20 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0017_alter_order_courier'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='managers_profit',
            field=models.PositiveIntegerField(blank=True, default=0, help_text="so'mda", null=True, verbose_name='Managerga (Temur) beriladigan pul'),
        ),
    ]