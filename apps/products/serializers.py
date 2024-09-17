from rest_framework import serializers

from apps.main.serializers import BrandSerializer
from apps.products.models import Product, CharacteristicGroup, Characteristic


class ProductSerializer(serializers.ModelSerializer):
    product_image = serializers.ImageField()
    brand = BrandSerializer()
    characteristics = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'uuid',
            'name',
            'product_image',
            'specs',
            'description',
            'sku',
            'price',
            'price_currency',
            'stock_quantity',
            'is_available',
            'brand',
            'characteristics',
        ]

    def get_characteristics(self, obj):
        queryset = obj.characteristic_groups.all()
        serializer = CharacteristicGroupSerializer(queryset, many=True)
        return serializer.data


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = [
            'title',
            'value',
        ]


class CharacteristicGroupSerializer(serializers.ModelSerializer):
    characteristic = CharacteristicSerializer(
        many=True, source='characteristics'
    )

    class Meta:
        model = CharacteristicGroup
        fields = [
            'name',
            'characteristic',
        ]
