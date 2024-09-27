from rest_framework import serializers

from apps.catalog.models import Category
from apps.products.models import Product


class ProductForCatalogSerializer(serializers.ModelSerializer):
    """
    Сериализатор товара для каталога
    """

    image = serializers.ImageField()

    class Meta:
        model = Product
        fields = [
            'uuid',
            'name',
            'image',
            'specs',
            'price',
            'priceCurrency',
            'stockQuantity',
            'isAvailable',
        ]


class RecursiveField(serializers.Serializer):
    """
    Рекурсивное поле для вложенных категорий.
    """

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    """
    Рекурсивный сериализатор категории.
    """

    image = serializers.ImageField()
    children = RecursiveField(many=True)
    products = ProductForCatalogSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['uuid', 'name', 'slug', 'image', 'children', 'products']
