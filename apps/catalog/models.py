import uuid
from typing import Any

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class MainCategory(models.Model):
    """
    Модель главной категории
    """

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, verbose_name='Slug'
    )
    name = models.CharField(
        max_length=256, verbose_name='Название главной категории'
    )
    image = models.ImageField(
        upload_to='main_category/',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(MainCategory, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Главная категория'
        verbose_name_plural = 'Главные категории'


class SubCategory(models.Model):
    """
    Модель подкатегории
    """

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, verbose_name='Slug'
    )
    name = models.CharField(
        max_length=256, verbose_name='Название подкатегории'
    )
    image = models.ImageField(
        upload_to='sub_category/',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )

    mainCategory = models.ForeignKey(
        MainCategory,
        related_name='subcategories',
        on_delete=models.CASCADE,
        verbose_name='Главная категория',
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.mainCategory} -> {self.name}'

    def get_absolute_url(self) -> str:
        return reverse('admin:catalog_subcategory_change', args=[str(self.id)])

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class ProductVariety(models.Model):
    """
    Модель разновидности товара
    """

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, verbose_name='Slug'
    )
    name = models.CharField(
        max_length=256, verbose_name='Название разновидности'
    )
    image = models.ImageField(
        upload_to='product_type/',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )

    subCategory = models.ForeignKey(
        SubCategory,
        related_name='product_varietys',
        on_delete=models.CASCADE,
        verbose_name='Подкатегория',
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(ProductVariety, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.subCategory} -> {self.name}'

    def get_absolute_url(self) -> str:
        return reverse(
            'admin:catalog_productvariety_change', args=[str(self.id)]
        )

    class Meta:
        verbose_name = 'Разновидность продукта'
        verbose_name_plural = 'Разновидность продуктов'


class ProductType(models.Model):
    """
    Модель типа товара
    """

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, verbose_name='Slug'
    )
    name = models.CharField(max_length=256, verbose_name='Название типа')
    image = models.ImageField(
        upload_to='product_type/',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )

    productVariety = models.ForeignKey(
        ProductVariety,
        related_name='product_types',
        on_delete=models.CASCADE,
        verbose_name='Разновидность продукта',
        null=True,
        blank=True,
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(ProductType, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.productVariety} -> {self.name}'

    def get_absolute_url(self) -> str:
        return reverse('admin:catalog_producttype_change', args=[str(self.id)])

    class Meta:
        verbose_name = 'Тип продукта'
        verbose_name_plural = 'Типы продуктов'


class ProductSubtype(models.Model):
    """
    Модель подтипа товара
    """

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, verbose_name='Slug'
    )
    name = models.CharField(max_length=256, verbose_name='Название подтипа')
    image = models.ImageField(
        upload_to='product_subtype/',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )

    productType = models.ForeignKey(
        ProductType,
        related_name='product_subtypes',
        on_delete=models.CASCADE,
        verbose_name='Тип продукта',
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(ProductSubtype, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.productType} -> {self.name}'

    def get_absolute_url(self) -> str:
        return reverse(
            'admin:catalog_productsubtype_change', args=[str(self.id)]
        )

    class Meta:
        verbose_name = 'Подтип продукта'
        verbose_name_plural = 'Подтипы продуктов'
