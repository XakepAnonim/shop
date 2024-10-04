import uuid

from django.db import models

from apps.main.models import Company
from apps.models import BaseModel
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


class Order(BaseModel):
    """
    Модель заказа
    """
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество товаров',
    )
    totalPrice = models.DecimalField(
        max_digits=9,
        decimal_places=0,
        verbose_name='Общая сумма',
    )
    deliveryType = models.CharField(
        max_length=25,
        choices=[
            ('pickup', 'Самовывоз'),
            ('delivery', 'Доставка'),
        ],
        default='pickup',
        verbose_name='Тип доставки',
    )
    paymentMethod = models.CharField(
        max_length=25,
        choices=[
            ('online', 'Онлайн'),
            ('cash', 'При получении'),
            ('credit', 'В кредит')
        ],
        default='online',
        verbose_name='Метод оплаты',
    )
    onlineMethod = models.CharField(
        max_length=25,
        choices=[
            ('sbp', 'СПБ'),
            ('yoomoney', 'Ю-money'),
            ('card', 'Карта'),
        ],
        default='sbp',
        verbose_name='Метод онлайн оплаты',
        blank=True,
        null=True,
    )
    deliveryAddress = models.CharField(
        max_length=255,
        verbose_name='Адрес доставки',
        blank=True,
        null=True,
    )
    deliveryCoordinates = models.CharField(
        max_length=255, verbose_name='Координаты доставки', blank=True, null=True,
    )
    status = models.CharField(
        max_length=100,
        choices=[
            ('pending', 'В ожидании'),
            ('accepted', 'Принято'),
            ('paid', 'Оплачено'),
            ('canceled', 'Отменено'),
            ('delayed', 'Задерживается'),
            ('delivery_point', 'В пункте выдачи'),
            ('delivered', 'Доставлено'),
        ],
        default='pending',
        verbose_name='Статус',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь',
        blank=True,
        null=True,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Компания',
        blank=True,
        null=True,
    )
    products = models.ManyToManyField(
        Product, verbose_name='Товары'
    )

    def __str__(self):
        return f"Заказ {self.id} от {self.user}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-id']
