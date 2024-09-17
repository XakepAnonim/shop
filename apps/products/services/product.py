import uuid

from django.shortcuts import get_object_or_404

from apps.products.models import Product


class ProductService:
    @staticmethod
    def get(uuid: uuid.uuid4, slug):
        return get_object_or_404(Product, uuid=uuid, slug=slug)
