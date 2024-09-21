import uuid

from django.db import models

from apps.products.models import Product
from apps.users.models import User


class Cart(models.Model):
    """
    Модель корзины
    """

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    count = models.PositiveSmallIntegerField(verbose_name='Количество товаров')
    total_price = models.DecimalField(
        max_digits=7, decimal_places=0, verbose_name='Общая цена'
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    products = models.ManyToManyField(
        Product,
        related_name='cart_products',
        verbose_name='Продукты',
    )

    def __str__(self):
        return f'Cart for {self.user}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
