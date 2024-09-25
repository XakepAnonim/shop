from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.catalog.serializers import ProductForCatalogSerializer
from apps.main.serializers import BrandForProductSerializer
from apps.products.models import (
    Characteristic,
    CharacteristicGroup,
    Product,
    WishlistProduct,
)


class CharacteristicSerializer(serializers.ModelSerializer):
    """
    Сериализатор групп характеристик товара
    """

    class Meta:
        model = Characteristic
        fields = [
            'title',
            'value',
        ]


class CharacteristicGroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор характеристик товара
    """

    characteristic = CharacteristicSerializer(
        many=True, source='characteristics'
    )

    class Meta:
        model = CharacteristicGroup
        fields = [
            'name',
            'characteristic',
        ]


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор товара
    """

    image = serializers.ImageField()
    brand = BrandForProductSerializer()
    characteristics = serializers.SerializerMethodField()

    @extend_schema_field(CharacteristicGroupSerializer(many=True))
    def get_characteristics(self, obj: Product) -> dict:
        queryset = obj.characteristic_groups.all()
        serializer = CharacteristicGroupSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Product
        fields = [
            'uuid',
            'name',
            'image',
            'specs',
            'description',
            'sku',
            'price',
            'priceCurrency',
            'stockQuantity',
            'isAvailable',
            'brand',
            'characteristics',
        ]


class WishlistProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор желаемых товаров пользователя
    """

    products = ProductForCatalogSerializer(many=True)

    class Meta:
        model = WishlistProduct
        fields = [
            'uuid',
            'count',
            'total_price',
            'products',
        ]
