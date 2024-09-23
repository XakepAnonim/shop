import uuid

from django.db import models

from apps.models import BaseModel
from apps.products.models import Product
from apps.users.models import User

PERIODS_CHOICES = (
    (1, 'Менее месяца'),
    (2, 'Не более года'),
    (3, 'Более года'),
)


class Opinion(BaseModel):
    """
    Модель мнения о товаре
    """

    advantages = models.TextField(verbose_name='Достоинства')
    disadvantages = models.TextField(verbose_name='Недостатки')
    commentary = models.TextField(verbose_name='Комментарий')
    problem = models.TextField(verbose_name='Проблема', blank=True, null=True)
    images = models.FileField(
        verbose_name='Фотографии и видео', blank=True, null=True
    )
    periods = models.CharField(
        max_length=16,
        choices=PERIODS_CHOICES,
        default=1,
        verbose_name='Срок использования',
    )
    likes = models.ManyToManyField(
        User, related_name='liked_opinions', blank=True, verbose_name='Лайки'
    )

    user = models.ForeignKey(
        User,
        related_name='opinions',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    product = models.ForeignKey(
        Product,
        related_name='opinions',
        on_delete=models.CASCADE,
        verbose_name='Товар',
    )

    def __str__(self):
        return f'{self.user} opinion on {self.product}'

    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = 'Мнение'
        verbose_name_plural = 'Мнения'


class OpinionComment(models.Model):
    """
    Модель комментариев к отзывам
    """

    user = models.ForeignKey(
        User,
        related_name='opinion_comments',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    opinion = models.ForeignKey(
        Opinion,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )
    text = models.TextField(verbose_name='Комментарий')
    likes = models.ManyToManyField(
        User, related_name='liked_comments', blank=True, verbose_name='Лайки'
    )

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'Комментарий {self.user} к отзыву {self.opinion}'

    class Meta:
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзывам'


class Grades(models.Model):
    """
    Оценки характеристик товаров
    """

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    title = models.CharField(max_length=52, verbose_name='Название оценки')
    grade = models.PositiveSmallIntegerField(
        max_length=5, verbose_name='Оценка'
    )
    opinion = models.ForeignKey(
        Opinion,
        related_name='grades',
        on_delete=models.CASCADE,
        verbose_name='Мнение',
    )

    def __str__(self):
        return f'{self.title}: {self.grade}'

    class Meta:
        verbose_name = 'Оценка характеристики'
        verbose_name_plural = 'Оценки характеристик'
