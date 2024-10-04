from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.main.models import Brand


class BrandService:
    """
    Сервис для работы с брендами
    """

    @staticmethod
    def get(name: str) -> Brand:
        """
        Получение бренда по названию
        """
        brand = get_object_or_404(Brand, name=name)
        return brand

    @staticmethod
    def get_all() -> QuerySet[Brand]:
        """
        Получение всех брендов
        """
        brands = Brand.objects.all()
        return brands
