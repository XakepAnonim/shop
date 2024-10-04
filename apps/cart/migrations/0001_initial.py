# Generated by Django 5.1.1 on 2024-10-04 07:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('total_price', models.DecimalField(decimal_places=0, default=0.0, max_digits=7, verbose_name='Общая цена')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Элемент корзины',
                'verbose_name_plural': 'Элементы корзины',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество товаров')),
                ('totalPrice', models.DecimalField(decimal_places=0, max_digits=9, verbose_name='Общая сумма')),
                ('deliveryType', models.CharField(choices=[('pickup', 'Самовывоз'), ('delivery', 'Доставка')], default='pickup', max_length=25, verbose_name='Тип доставки')),
                ('paymentMethod', models.CharField(choices=[('online', 'Онлайн'), ('cash', 'При получении'), ('credit', 'В кредит')], default='online', max_length=25, verbose_name='Метод оплаты')),
                ('onlineMethod', models.CharField(blank=True, choices=[('sbp', 'СПБ'), ('yoomoney', 'Ю-money'), ('card', 'Карта')], default='sbp', max_length=25, null=True, verbose_name='Метод онлайн оплаты')),
                ('deliveryAddress', models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес доставки')),
                ('deliveryCoordinates', models.CharField(blank=True, max_length=255, null=True, verbose_name='Координаты доставки')),
                ('status', models.CharField(choices=[('pending', 'В ожидании'), ('accepted', 'Принято'), ('paid', 'Оплачено'), ('canceled', 'Отменено'), ('delayed', 'Задерживается'), ('delivery_point', 'В пункте выдачи'), ('delivered', 'Доставлено')], default='pending', max_length=100, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-id'],
            },
        ),
    ]
