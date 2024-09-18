import uuid
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class MainCategory(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    name = models.CharField(
        max_length=256, verbose_name='Название главной категории'
    )
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, verbose_name='Slug'
    )
    image = models.ImageField(
        upload_to='main_category/',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )
    description = models.TextField(blank=True, verbose_name='Описание')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(MainCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Главная категория'
        verbose_name_plural = 'Главные категории'


class SubCategory(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    main_category = models.ForeignKey(
        MainCategory,
        related_name='subcategories',
        on_delete=models.CASCADE,
        verbose_name='Главная категория',
    )
    name = models.CharField(
        max_length=256, verbose_name='Название подкатегории'
    )
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, verbose_name='Slug'
    )
    image = models.ImageField(
        upload_to='sub_category/',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )
    description = models.TextField(blank=True, verbose_name='Описание')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.main_category} -> {self.name}'

    def get_absolute_url(self):
        return reverse('admin:catalog_subcategory_change', args=[str(self.id)])

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class ProductVariety(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    sub_category = models.ForeignKey(
        SubCategory,
        related_name='product_varietys',
        on_delete=models.CASCADE,
        verbose_name='Подкатегория',
    )
    name = models.CharField(
        max_length=256, verbose_name='Название разновидности'
    )
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, verbose_name='Slug'
    )
    image = models.ImageField(
        upload_to='product_type/',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )
    description = models.TextField(blank=True, verbose_name='Описание')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(ProductVariety, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.sub_category} -> {self.name}'

    def get_absolute_url(self):
        return reverse(
            'admin:catalog_productvariety_change', args=[str(self.id)]
        )

    class Meta:
        verbose_name = 'Разновидность продукта'
        verbose_name_plural = 'Разновидность продуктов'


class ProductType(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    product_variety = models.ForeignKey(
        ProductVariety,
        related_name='product_types',
        on_delete=models.CASCADE,
        verbose_name='Разновидность продукта',
        null=True,
        blank=True,
    )
    products = models.ManyToManyField(
        'products.Product', verbose_name='Товары'
    )
    name = models.CharField(max_length=256, verbose_name='Название типа')
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, verbose_name='Slug'
    )
    image = models.ImageField(
        upload_to='product_type/',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )
    description = models.TextField(blank=True, verbose_name='Описание')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(ProductType, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.product_variety} -> {self.name}'

    def get_absolute_url(self):
        return reverse('admin:catalog_producttype_change', args=[str(self.id)])

    class Meta:
        verbose_name = 'Тип продукта'
        verbose_name_plural = 'Типы продуктов'


class ProductSubtype(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    product_type = models.ForeignKey(
        ProductType,
        related_name='product_subtypes',
        on_delete=models.CASCADE,
        verbose_name='Тип продукта',
    )
    products = models.ManyToManyField(
        'products.Product', verbose_name='Товары'
    )
    name = models.CharField(max_length=256, verbose_name='Название подтипа')
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, verbose_name='Slug'
    )
    image = models.ImageField(
        upload_to='product_subtype/',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )
    description = models.TextField(blank=True, verbose_name='Описание')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(ProductSubtype, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.product_type} -> {self.name}'

    def get_absolute_url(self):
        return reverse(
            'admin:catalog_productsubtype_change', args=[str(self.id)]
        )

    class Meta:
        verbose_name = 'Подтип продукта'
        verbose_name_plural = 'Подтипы продуктов'
