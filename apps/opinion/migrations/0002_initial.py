# Generated by Django 5.1.1 on 2024-09-23 21:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('opinion', '0001_initial'),
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='opinion',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='disliked_opinions', to=settings.AUTH_USER_MODEL, verbose_name='Дизлайки'),
        ),
        migrations.AddField(
            model_name='opinion',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_opinions', to=settings.AUTH_USER_MODEL, verbose_name='Лайки'),
        ),
        migrations.AddField(
            model_name='opinion',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opinions', to='products.product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='opinion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opinions', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='grades',
            name='opinion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='opinion.opinion', verbose_name='Мнение'),
        ),
        migrations.AddField(
            model_name='opinioncomment',
            name='dislikes',
            field=models.ManyToManyField(related_name='disliked_comments', to=settings.AUTH_USER_MODEL, verbose_name='Дизлайки'),
        ),
        migrations.AddField(
            model_name='opinioncomment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_comments', to=settings.AUTH_USER_MODEL, verbose_name='Лайки'),
        ),
        migrations.AddField(
            model_name='opinioncomment',
            name='opinion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='opinion.opinion', verbose_name='Отзыв'),
        ),
        migrations.AddField(
            model_name='opinioncomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opinion_comments', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
