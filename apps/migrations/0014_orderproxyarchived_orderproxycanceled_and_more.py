# Generated by Django 5.1.1 on 2024-10-11 04:56

import django.db.models.deletion
import managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0013_rename_user_transaction_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProxyArchived',
            fields=[
                ('order_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='apps.order')),
            ],
            options={
                'abstract': False,
            },
            bases=('apps.order',),
        ),
        migrations.CreateModel(
            name='OrderProxyCanceled',
            fields=[
                ('order_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='apps.order')),
            ],
            options={
                'abstract': False,
            },
            bases=('apps.order',),
        ),
        migrations.CreateModel(
            name='OrderProxyDelivered',
            fields=[
                ('order_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='apps.order')),
            ],
            options={
                'abstract': False,
            },
            bases=('apps.order',),
        ),
        migrations.CreateModel(
            name='OrderProxyDelivering',
            fields=[
                ('order_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='apps.order')),
            ],
            options={
                'abstract': False,
            },
            bases=('apps.order',),
        ),
        migrations.CreateModel(
            name='OrderProxyNew',
            fields=[
                ('order_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='apps.order')),
            ],
            options={
                'abstract': False,
            },
            bases=('apps.order',),
        ),
        migrations.CreateModel(
            name='OrderProxyReady',
            fields=[
                ('order_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='apps.order')),
            ],
            options={
                'abstract': False,
            },
            bases=('apps.order',),
        ),
        migrations.CreateModel(
            name='UserProxyAdminModel',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('apps.user',),
            managers=[
                ('objects', managers.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserProxyDriverModel',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('apps.user',),
            managers=[
                ('objects', managers.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserProxyManagerModel',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('apps.user',),
            managers=[
                ('objects', managers.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserProxyOperatorModel',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('apps.user',),
            managers=[
                ('objects', managers.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserProxyUserModel',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('apps.user',),
            managers=[
                ('objects', managers.CustomUserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.PositiveIntegerField(db_default=0, verbose_name='Userning beriladigan pul miqdori'),
        ),
        migrations.CreateModel(
            name='CurrierProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type', models.CharField(max_length=50, verbose_name='Vehicle Type')),
                ('license_number', models.CharField(max_length=100, verbose_name='License Number')),
                ('availability_status', models.BooleanField(default=True, verbose_name='Is Available')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='currier_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
