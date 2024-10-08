from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.opinion.models import Opinion
from apps.products.models import Product
from apps.users.models import User


class OpinionService:
    """
    Сервис для работы с отзывами
    """

    @staticmethod
    def get(opinion_uuid: str) -> Opinion:
        """
        Получение отзыва по uuid
        """
        opinion = get_object_or_404(Opinion, uuid=opinion_uuid)
        return opinion

    @staticmethod
    def filter(product: Product) -> QuerySet[Opinion]:
        """
        Получение отзывов по товарам
        """
        opinions = Opinion.objects.filter(product=product)
        return opinions

    @staticmethod
    def add_or_remove_likes(user: User, opinion: Opinion) -> None:
        """
        Добавление или удаление лайка
        """
        if user in opinion.likes.all():
            opinion.likes.remove(user)
        else:
            opinion.likes.add(user)
            opinion.dislikes.remove(user)

    @staticmethod
    def add_or_remove_dislikes(user: User, opinion: Opinion) -> None:
        """
        Добавление или удаление дизлайка
        """
        if user in opinion.dislikes.all():
            opinion.dislikes.remove(user)
        else:
            opinion.dislikes.add(user)
            opinion.likes.remove(user)
