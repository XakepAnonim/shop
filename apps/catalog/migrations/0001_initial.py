# Generated by Django 5.1.1 on 2024-09-20 12:57

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('slug', models.SlugField(blank=True, max_length=256, unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=256, verbose_name='Название главной категории')),
                ('image', models.ImageField(blank=True, null=True, upload_to='main_category/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Главная категория',
                'verbose_name_plural': 'Главные категории',
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('slug', models.SlugField(blank=True, max_length=256, unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=256, verbose_name='Название типа')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_type/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Тип продукта',
                'verbose_name_plural': 'Типы продуктов',
            },
        ),
        migrations.CreateModel(
            name='ProductVariety',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('slug', models.SlugField(blank=True, max_length=256, unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=256, verbose_name='Название разновидности')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_type/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Разновидность продукта',
                'verbose_name_plural': 'Разновидность продуктов',
            },
        ),
        migrations.CreateModel(
            name='ProductSubtype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('slug', models.SlugField(blank=True, max_length=256, unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=256, verbose_name='Название подтипа')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_subtype/', verbose_name='Изображение')),
                ('productType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_subtypes', to='catalog.producttype', verbose_name='Тип продукта')),
            ],
            options={
                'verbose_name': 'Подтип продукта',
                'verbose_name_plural': 'Подтипы продуктов',
            },
        ),
        migrations.AddField(
            model_name='producttype',
            name='productVariety',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_types', to='catalog.productvariety', verbose_name='Разновидность продукта'),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('slug', models.SlugField(blank=True, max_length=256, unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=256, verbose_name='Название подкатегории')),
                ('image', models.ImageField(blank=True, null=True, upload_to='sub_category/', verbose_name='Изображение')),
                ('mainCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='catalog.maincategory', verbose_name='Главная категория')),
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
            },
        ),
        migrations.AddField(
            model_name='productvariety',
            name='subCategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_varietys', to='catalog.subcategory', verbose_name='Подкатегория'),
        ),
    ]
