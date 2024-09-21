from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.main.models import Brand


class BrandService:
    @staticmethod
    def get(name: str) -> Brand:
        brand = get_object_or_404(Brand, name=name)
        return brand

    @staticmethod
    def get_all() -> QuerySet[Brand]:
        brands = Brand.objects.all()
        return brands
