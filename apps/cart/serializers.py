from rest_framework import serializers
from apps.cart.models import CartItem, Cart
from apps.catalog.serializers import ProductForCatalogSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор корзины
    """

    product = ProductForCatalogSerializer()

    class Meta:
        model = CartItem
        fields = ['uuid', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    """
    Сериализатор корзины
    """

    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = [
            'uuid',
            'total_price',
            'items',
        ]
