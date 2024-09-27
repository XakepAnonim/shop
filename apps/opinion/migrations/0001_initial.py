# Generated by Django 5.1.1 on 2024-09-27 11:50

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('text', models.TextField(verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.CreateModel(
            name='Grades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('title', models.CharField(max_length=52, verbose_name='Название оценки')),
                ('grade', models.PositiveSmallIntegerField(verbose_name='Оценка')),
            ],
            options={
                'verbose_name': 'Оценка характеристики',
                'verbose_name_plural': 'Оценки характеристик',
            },
        ),
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('advantages', models.TextField(verbose_name='Достоинства')),
                ('disadvantages', models.TextField(verbose_name='Недостатки')),
                ('commentary', models.TextField(verbose_name='Комментарий')),
                ('problem', models.TextField(blank=True, null=True, verbose_name='Проблема')),
                ('images', models.FileField(blank=True, null=True, upload_to='', verbose_name='Фотографии и видео')),
                ('periods', models.CharField(choices=[('Менее месяца', 'Менее месяца'), ('Не более года', 'Не более года'), ('Более года', 'Более года')], max_length=16, verbose_name='Срок использования')),
            ],
            options={
                'verbose_name': 'Мнение',
                'verbose_name_plural': 'Мнения',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('title', models.TextField(max_length=50, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Подробно опишите Вашу проблему')),
            ],
            options={
                'verbose_name': 'Вопрос к товару',
                'verbose_name_plural': 'Вопросы к товарам',
            },
        ),
    ]
