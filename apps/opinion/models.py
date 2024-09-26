import uuid

from django.db import models
from django.urls import reverse

from apps.models import BaseModel
from apps.products.models import Product
from apps.users.models import User

PERIODS_CHOICES = (
    ('Менее месяца', 'Менее месяца'),
    ('Не более года', 'Не более года'),
    ('Более года', 'Более года'),
)


class BaseModelOpinion(BaseModel):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    likes = models.ManyToManyField(
        User,
        related_name='liked_%(class)s',
        verbose_name='Лайки',
        blank=True,
    )
    dislikes = models.ManyToManyField(
        User,
        related_name='disliked_%(class)s',
        verbose_name='Дизлайки',
        blank=True,
    )
    user = models.ForeignKey(
        User,
        related_name='%(class)s',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    def __str__(self) -> str:
        return f'{self.__class__.__name__} от {self.user}'

    @property
    def total_likes(self) -> int:
        return self.likes.count() - self.dislikes.count()

    class Meta:
        abstract = True


class Opinion(BaseModelOpinion):
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
        verbose_name='Срок использования',
    )

    product = models.ForeignKey(
        Product,
        related_name='opinions',
        on_delete=models.CASCADE,
        verbose_name='Товар',
    )

    def __str__(self) -> str:
        return f'{self.user} отзыв к товару {self.product}'

    def get_absolute_url(self) -> str:
        return reverse('admin:opinion_opinion_change', args=[str(self.id)])

    class Meta:
        verbose_name = 'Мнение'
        verbose_name_plural = 'Мнения'


class Question(BaseModelOpinion):
    title = models.TextField(max_length=50, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Подробно опишите Вашу проблему')

    product = models.ForeignKey(
        Product,
        related_name='questions',
        on_delete=models.CASCADE,
        verbose_name='Товар',
    )

    def __str__(self) -> str:
        return f'Вопрос от {self.user} к товару {self.product}'

    def get_absolute_url(self) -> str:
        return reverse('admin:opinion_question_change', args=[str(self.id)])

    class Meta:
        verbose_name = 'Вопрос к товару'
        verbose_name_plural = 'Вопросы к товарам'


class Comment(BaseModelOpinion):
    """
    Модель комментариев к отзывам
    """

    text = models.TextField(verbose_name='Комментарий')

    opinion = models.ForeignKey(
        Opinion,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        blank=True,
        null=True,
    )
    question = models.ForeignKey(
        Question,
        related_name='questions',
        on_delete=models.CASCADE,
        verbose_name='Вопрос',
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        if self.opinion:
            return f'Комментарий {self.user} к отзыву {self.opinion}'
        elif self.question:
            return f'Комментарий {self.user} к вопросу {self.question}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Grades(models.Model):
    """
    Оценки характеристик товаров
    """

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    title = models.CharField(max_length=52, verbose_name='Название оценки')
    grade = models.PositiveSmallIntegerField(verbose_name='Оценка')
    opinion = models.ForeignKey(
        Opinion,
        related_name='grades',
        on_delete=models.CASCADE,
        verbose_name='Мнение',
    )

    def __str__(self) -> str:
        return f'{self.title}: {self.grade}'

    class Meta:
        verbose_name = 'Оценка характеристики'
        verbose_name_plural = 'Оценки характеристик'
