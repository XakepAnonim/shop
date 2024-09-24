import uuid

from django.db import models
from django.urls import reverse

from apps.models import BaseModel


class Company(BaseModel, models.Model):
    """
    Модель компании
    """

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    name = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(max_length=500, verbose_name='Описание')

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('admin:main_company_change', args=[str(self.id)])

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Brand(BaseModel, models.Model):
    """
    Модель брэнда
    """

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    name = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(max_length=1500, verbose_name='Описание')
    image = models.ImageField(
        upload_to='brand/',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )

    company = models.ForeignKey(
        Company,
        related_name='brands',
        on_delete=models.CASCADE,
        verbose_name='Компания',
    )

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('admin:main_brand_change', args=[str(self.id)])

    class Meta:
        verbose_name = 'Брэнд'
        verbose_name_plural = 'Брэнды'
