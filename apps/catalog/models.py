import uuid
from typing import Any

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from unidecode import unidecode


class Category(MPTTModel):
    """
    Модель категории с поддержкой иерархии.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    name = models.CharField(
        max_length=256, unique=True, verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, verbose_name='Slug'
    )
    image = models.ImageField(
        upload_to='categories/',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория',
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)
        # cache.delete('all_categories')

    def generate_unique_slug(self) -> str:
        base_slug = slugify(unidecode(self.name))
        slug = base_slug
        num = 1
        while Category.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{num}'
            num += 1
        return slug

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('catalog:category_detail', args=[str(self.id)])

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
