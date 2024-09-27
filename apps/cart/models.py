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
    total_price = models.DecimalField(
        max_digits=7,
        decimal_places=0,
        default=0.00,
        verbose_name='Общая цена',
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    def __str__(self) -> str:
        return f'Корзина пользователя {self.user}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    """
    Промежуточная модель для хранения товаров в корзине и их количества.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    product = models.ForeignKey(
        Product,
        related_name='cart_items',
        on_delete=models.CASCADE,
        verbose_name='Продукт',
    )
    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='Корзина',
    )
    quantity = models.PositiveIntegerField(
        default=1, verbose_name='Количество'
    )

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    class Meta:
        unique_together = ('product', 'cart')
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
