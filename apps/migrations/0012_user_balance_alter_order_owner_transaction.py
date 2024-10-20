# Generated by Django 5.1.1 on 2024-10-07 11:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0011_alter_order_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.PositiveIntegerField(db_default=0, verbose_name='Userning balansi'),
        ),
        migrations.AlterField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Mahsulot Beruvchi'),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan Vaqti')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan Vaqti')),
                ('amount', models.PositiveIntegerField(db_default=0, verbose_name='Userning balansi')),
                ('card_number', models.CharField(max_length=16, verbose_name='Userning Karta Raqami')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Tolov xabari')),
                ('image', models.ImageField(blank=True, null=True, upload_to='transactons/%Y/%m/%d', verbose_name='Tolov rasmi')),
                ('status', models.CharField(choices=[('pending', 'PENDING'), ('canceled', 'CANCELED'), ('paid', 'PAID'), ('error', 'ERROR')], default='pending', max_length=10, verbose_name='Tolov Statusi')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="Mablag'gning egasi")),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
