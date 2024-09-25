# Generated by Django 5.1.1 on 2024-09-25 12:49

import django.db.models.deletion
import phonenumber_field.modelfields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('codename', models.CharField(max_length=250)),
                ('role', models.CharField(choices=[('admin', 'Администратор'), ('company', 'Компания')], max_length=255)),
            ],
            options={
                'verbose_name': 'Права',
                'verbose_name_plural': 'Права',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='Почта')),
                ('firstName', models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя')),
                ('lastName', models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилия')),
                ('phoneNumber', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=15, null=True, region=None, unique=True, verbose_name='Номер телефона')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Фото')),
                ('isStaff', models.BooleanField(default=False, verbose_name='Администратор?')),
                ('isCompany', models.BooleanField(default=False, verbose_name='Компания?')),
                ('approvedPhone', models.BooleanField(default=False, verbose_name='Подтвержден номер телефона?')),
                ('approvedEmail', models.BooleanField(default=False, verbose_name='Подтверждена почта?')),
                ('dateOfBirth', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Адрес')),
                ('secretKey', models.CharField(blank=True, max_length=32, null=True)),
                ('language', models.CharField(choices=[('en', 'English'), ('ru', 'Russian')], default='ru', max_length=10, verbose_name='Язык')),
                ('company', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.company', verbose_name='Компания')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('permissions', models.ManyToManyField(blank=True, to='users.permission', verbose_name='Права')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('authSSID', models.CharField(max_length=255, unique=True, verbose_name='Auth SSID')),
                ('deviceType', models.CharField(max_length=50, verbose_name='Тип устройства')),
                ('deviceName', models.CharField(max_length=255, verbose_name='Имя устройства')),
                ('os', models.CharField(max_length=50, verbose_name='Операционная система')),
                ('browser', models.CharField(max_length=50, verbose_name='Браузер')),
                ('ip', models.CharField(max_length=20, verbose_name='IP-адрес')),
                ('cityName', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=10, null=True, verbose_name='Страна')),
                ('isCurrent', models.BooleanField(default=True, verbose_name='Активен?')),
                ('userAgent', models.CharField(max_length=255, verbose_name='User Agent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Сеанс пользователя',
                'verbose_name_plural': 'Сеансы пользователей',
            },
        ),
    ]
