# Generated by Django 5.1.1 on 2024-09-29 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0003_stream'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='payment_referral',
            field=models.PositiveIntegerField(blank=True, default=0, help_text="so'mda", null=True, verbose_name='Chegirma'),
        ),
    ]
