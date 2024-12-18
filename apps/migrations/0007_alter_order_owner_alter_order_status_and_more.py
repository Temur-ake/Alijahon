# Generated by Django 5.1.1 on 2024-10-04 05:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0006_alter_order_status_alter_stream_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('yangi', 'YANGI'), ('Dastavkaga tayyor', 'DASTAVKAGA TAYYOR'), ('yetkazilmoqda', 'YETKAZILMOQDA'), ('yetkazib_berildi', 'YETKAZIB_BERILDI'), ('telefon_kotarmadi', 'TELEFON_KOTARMADI'), ('bekor_qilindi', 'BEKOR_QILINDI'), ('arxivlandi', 'ARXIVLANDI')], default='yangi', max_length=255),
        ),
        migrations.AlterField(
            model_name='stream',
            name='discount',
            field=models.PositiveSmallIntegerField(db_default=0),
        ),
    ]
