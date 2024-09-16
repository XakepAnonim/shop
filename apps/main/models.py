from django.db import models
from django.urls import reverse

from apps.models import BaseModel


class Company(BaseModel, models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(max_length=500, verbose_name='Описание')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('admin:main_company_change', args=[str(self.id)])

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Brand(BaseModel, models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    company = models.ForeignKey(
        Company,
        related_name='brands',
        on_delete=models.CASCADE,
        verbose_name='Компания',
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('admin:main_brand_change', args=[str(self.id)])

    class Meta:
        verbose_name = 'Брэнд'
        verbose_name_plural = 'Брэнды'
