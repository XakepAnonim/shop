from typing import Any

from django.db import transaction
from rest_framework import serializers
from apps.cart.models import CartItem, Cart, Order
from apps.catalog.serializers import ProductForCatalogSerializer
from apps.main.serializers import CompanySerializer
from apps.users.serializers import AuthUserSerializer


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


class OrderDataValidator(serializers.Serializer):
    deliveryType = serializers.ChoiceField(choices=['pickup', 'delivery'], required=True)
    paymentMethod = serializers.ChoiceField(choices=['online', 'cash', 'credit'], required=True)
    onlineMethod = serializers.ChoiceField(choices=['sbp', 'yoomoney', 'card'], required=False)
    deliveryAddress = serializers.CharField(max_length=255, required=False)
    deliveryCoordinates = serializers.CharField(max_length=255, required=False)

    def validate(self, data):
        if (
            data['deliveryType'] == 'delivery'
            and not (data.get('deliveryAddress')
            and data.get('deliveryCoordinates'))
        ):
            raise serializers.ValidationError("Адрес доставки обязателен при выборе доставки.")
        if data['paymentMethod'] == 'online' and not data.get('onlineMethod'):
            raise serializers.ValidationError("Метод оплаты обязателен при выборе онлайн.")
        return data


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели заказа
    """

    class Meta:
        model = Order
        fields = [
            'uuid',
            'quantity',
            'totalPrice',
            'deliveryType',
            'paymentMethod',
            'onlineMethod',
            'deliveryAddress',
            'deliveryCoordinates',
            'status',
            'user',
        ]
