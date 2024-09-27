# Generated by Django 5.1.1 on 2024-09-27 11:50

import django.db.models.deletion
import mptt.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacteristicGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название группы')),
            ],
            options={
                'verbose_name': 'Группа характеристики',
                'verbose_name_plural': 'Группы характеристики',
            },
        ),
        migrations.CreateModel(
            name='Characteristic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Название характеристики')),
                ('value', models.CharField(max_length=1024, verbose_name='Значение')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristics', to='products.characteristicgroup', verbose_name='Группа характеристик')),
            ],
            options={
                'verbose_name': 'Характеристика',
                'verbose_name_plural': 'Характеристики',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('slug', models.SlugField(blank=True, max_length=256, unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Изображение')),
                ('specs', models.TextField(max_length=150, verbose_name='Тех. Характеристики')),
                ('description', models.TextField(max_length=1500, verbose_name='Описание')),
                ('sku', models.PositiveBigIntegerField(unique=True, verbose_name='Артикул')),
                ('price', models.DecimalField(decimal_places=0, max_digits=7, verbose_name='Цена')),
                ('priceCurrency', models.CharField(choices=[('RUB', 'RUB'), ('US', 'US'), ('YEN', 'YEN'), ('EURO', 'EURO'), ('YUAN', 'YUAN')], default='RUB', max_length=4, verbose_name='Валюта')),
                ('stockQuantity', models.PositiveIntegerField(verbose_name='Кол-во на складе')),
                ('isAvailable', models.BooleanField(verbose_name='В наличии?')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='main.brand', verbose_name='Бренд')),
                ('category', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='catalog.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.AddField(
            model_name='characteristicgroup',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristic_groups', to='products.product', verbose_name='Продукт'),
        ),
        migrations.CreateModel(
            name='WishlistProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('count', models.PositiveSmallIntegerField(verbose_name='Количество товаров')),
                ('total_price', models.DecimalField(decimal_places=0, max_digits=7, verbose_name='Общая цена')),
                ('products', models.ManyToManyField(blank=True, related_name='wishlist_products', to='products.product', verbose_name='Продукты')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранные',
            },
        ),
    ]
