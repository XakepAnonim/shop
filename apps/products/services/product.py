import uuid as py_uuid

from django.shortcuts import get_object_or_404

from apps.products.models import Product


class ProductService:
    @staticmethod
    def get(uuid: py_uuid.uuid4, slug: str) -> Product:
        """
        Получение товара по uuid и slug
        """
        product = get_object_or_404(Product, uuid=uuid, slug=slug)
        return product
