from django.shortcuts import get_object_or_404

from apps.products.models import Product


class ProductService:
    """
    Сервис для работы с товарами
    """

    @staticmethod
    def get(product_uuid: str, slug: str) -> Product:
        """
        Получение товара по uuid и slug
        """
        product = get_object_or_404(Product, uuid=product_uuid, slug=slug)
        return product

    @staticmethod
    def get_only_uuid(product_uuid: str) -> Product:
        """
        Получение товара по uuid
        """
        product = get_object_or_404(Product, uuid=product_uuid)
        return product
