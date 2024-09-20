from drf_spectacular.utils import extend_schema_field
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


class ProductSubtypeSerializer(serializers.ModelSerializer):
    """
    Сериализатор подтипа товара
    """

    image = serializers.ImageField()
    childs = serializers.SerializerMethodField()

    @extend_schema_field(ProductForCatalogSerializer(many=True))
    def get_childs(self, obj):
        queryset = obj.products_in_subtype.all()
        serializer = ProductForCatalogSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = ProductSubtype
        fields = [
            'uuid',
            'name',
            'slug',
            'image',
            'childs',
        ]


class ProductTypeSerializer(serializers.ModelSerializer):
    """
    Сериализатор типа товара
    """

    image = serializers.ImageField()
    childs = serializers.SerializerMethodField()

    @extend_schema_field(
        serializers.ListSerializer(child=serializers.DictField())
    )
    def get_childs(self, obj):
        subtypes = obj.product_subtypes.all()
        if subtypes:
            serializer = ProductSubtypeSerializer(subtypes, many=True)
            return serializer.data
        else:
            products = obj.products_in_type.all()
            serializer = ProductForCatalogSerializer(products, many=True)
            return serializer.data

    class Meta:
        model = ProductType
        fields = [
            'uuid',
            'name',
            'slug',
            'image',
            'childs',
        ]


class ProductVarietySerializer(serializers.ModelSerializer):
    """
    Сериализатор разновидности товара
    """

    image = serializers.ImageField()
    childs = serializers.SerializerMethodField()

    @extend_schema_field(ProductTypeSerializer(many=True))
    def get_childs(self, obj):
        queryset = obj.product_types.all()
        serializer = ProductTypeSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = ProductVariety
        fields = [
            'uuid',
            'name',
            'slug',
            'image',
            'childs',
        ]


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор подкатегории
    """

    image = serializers.ImageField()
    childs = serializers.SerializerMethodField()

    @extend_schema_field(ProductVarietySerializer(many=True))
    def get_childs(self, obj):
        queryset = obj.product_varietys.all()
        serializer = ProductVarietySerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = SubCategory
        fields = [
            'uuid',
            'name',
            'slug',
            'image',
            'childs',
        ]


class MainCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категории
    """

    image = serializers.ImageField()
    childs = serializers.SerializerMethodField()

    @extend_schema_field(SubCategorySerializer(many=True))
    def get_childs(self, obj):
        queryset = obj.subcategories.all()
        serializer = SubCategorySerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = MainCategory
        fields = ['uuid', 'name', 'slug', 'image', 'childs']
