import uuid

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode

from apps.catalog.models import ProductType, ProductSubtype
from apps.models import BaseModel

CURRENCY_TYPE = (
    ('RUB', 'RUB'),
    ('US', 'US'),
    ('YEN', 'YEN'),
    ('EURO', 'EURO'),
    ('YUAN', 'YUAN'),
)


class Product(BaseModel):
    """
    Модель товара
    """

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, verbose_name='Slug'
    )
    name = models.CharField(max_length=256, verbose_name='Название')
    image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )
    specs = models.TextField(
        max_length=150, verbose_name='Тех. Характеристики'
    )
    description = models.TextField(max_length=1500, verbose_name='Описание')
    sku = models.PositiveBigIntegerField(unique=True, verbose_name='Артикул')
    price = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='Цена'
    )
    priceCurrency = models.CharField(
        max_length=4,
        choices=CURRENCY_TYPE,
        default='RUB',
        verbose_name='Валюта',
    )
    stockQuantity = models.PositiveIntegerField(
        verbose_name='Кол-во на складе'
    )
    isAvailable = models.BooleanField(verbose_name='В наличии?')

    brand = models.ForeignKey(
        'main.Brand',
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name='Бренд',
    )
    productType = models.ForeignKey(
        ProductType,
        related_name='products_in_type',
        on_delete=models.CASCADE,
        verbose_name='Тип продукта',
        null=True,
        blank=True,
    )
    productSubtype = models.ForeignKey(
        ProductSubtype,
        related_name='products_in_subtype',
        on_delete=models.CASCADE,
        verbose_name='Подтип продукта',
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = self.generate_unique_sku()
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super(Product, self).save(*args, **kwargs)

    def generate_unique_sku(self):
        import random

        while True:
            sku = random.randint(100000, 999999)
            if not Product.objects.filter(sku=sku).exists():
                return sku

    def generate_unique_slug(self):
        base_slug = slugify(unidecode(self.name))
        slug = base_slug
        num = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{num}'
            num += 1
        return slug

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('admin:products_product_change', args=[str(self.id)])

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class CharacteristicGroup(models.Model):
    """
    Модель группы характеристик товара
    """

    name = models.CharField(max_length=256, verbose_name='Название группы')

    product = models.ForeignKey(
        Product,
        related_name='characteristic_groups',
        on_delete=models.CASCADE,
        verbose_name='Продукт',
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'admin:products_characteristicgroup_change', args=[str(self.id)]
        )

    class Meta:
        verbose_name = 'Группа характеристики'
        verbose_name_plural = 'Группы характеристики'


class Characteristic(models.Model):
    """
    Модель характеристики товара
    """

    title = models.CharField(
        max_length=256, verbose_name='Название характеристики'
    )
    value = models.CharField(max_length=1024, verbose_name='Значение')

    group = models.ForeignKey(
        CharacteristicGroup,
        related_name='characteristics',
        on_delete=models.CASCADE,
        verbose_name='Группа характеристик',
    )

    def __str__(self):
        return f'{self.title}: {self.value}'

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
