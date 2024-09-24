from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.opinion.models import Opinion
from apps.products.models import Product
from apps.users.models import User


class OpinionService:
    @staticmethod
    def get(opinion_uuid: str) -> Opinion:
        opinion = get_object_or_404(Opinion, uuid=opinion_uuid)
        return opinion

    @staticmethod
    def filter(product: Product) -> QuerySet[Opinion]:
        opinions = Opinion.objects.filter(product=product)
        return opinions

    @staticmethod
    def add_or_remove_likes(user: User, opinion: Opinion) -> None:
        if user in opinion.likes.all():
            opinion.likes.remove(user)
        else:
            opinion.likes.add(user)
            opinion.dislikes.remove(user)
