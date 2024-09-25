from rest_framework import serializers

from apps.cart.models import Cart
from apps.catalog.serializers import ProductForCatalogSerializer


class CartSerializer(serializers.ModelSerializer):
    """
    Сериализатор корзины
    """

    products = ProductForCatalogSerializer(many=True)

    class Meta:
        model = Cart
        fields = [
            'uuid',
            'count',
            'total_price',
            'products',
        ]
