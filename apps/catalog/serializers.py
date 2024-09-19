from rest_framework import serializers

from apps.catalog.models import (
    MainCategory,
    SubCategory,
    ProductVariety,
    ProductType,
    ProductSubtype,
)
from apps.products.models import Product


class ProductForCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'uuid',
            'name',
            'product_image',
            'specs',
            'price',
            'price_currency',
            'stock_quantity',
            'is_available',
        ]


class MainCategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    childs = serializers.SerializerMethodField()

    class Meta:
        model = MainCategory
        fields = ['uuid', 'name', 'slug', 'image', 'childs']

    def get_childs(self, obj):
        queryset = obj.subcategories.all()
        serializer = SubCategorySerializer(queryset, many=True)
        return serializer.data


class SubCategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    childs = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = [
            'uuid',
            'name',
            'slug',
            'image',
            'childs',
        ]

    def get_childs(self, obj):
        queryset = obj.product_varietys.all()
        serializer = ProductVarietySerializer(queryset, many=True)
        return serializer.data


class ProductVarietySerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    childs = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariety
        fields = [
            'uuid',
            'name',
            'slug',
            'image',
            'childs',
        ]

    def get_childs(self, obj):
        queryset = obj.product_types.all()
        serializer = ProductTypeSerializer(queryset, many=True)
        return serializer.data


class ProductTypeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    childs = serializers.SerializerMethodField()

    class Meta:
        model = ProductType
        fields = [
            'uuid',
            'name',
            'slug',
            'image',
            'childs',
        ]

    def get_childs(self, obj):
        subtypes = obj.product_subtypes.all()
        if subtypes:
            serializer = ProductSubtypeSerializer(subtypes, many=True)
            return serializer.data
        else:
            products = obj.products_in_type.all()
            serializer = ProductForCatalogSerializer(products, many=True)
            return serializer.data


class ProductSubtypeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    childs = serializers.SerializerMethodField()

    class Meta:
        model = ProductSubtype
        fields = [
            'uuid',
            'name',
            'slug',
            'image',
            'childs',
        ]

    def get_childs(self, obj):
        queryset = obj.products_in_subtype.all()
        serializer = ProductForCatalogSerializer(queryset, many=True)
        return serializer.data
