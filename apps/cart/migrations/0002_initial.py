# Generated by Django 5.1.1 on 2024-09-26 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(related_name='cart_products', to='products.product', verbose_name='Продукты'),
        ),
    ]
