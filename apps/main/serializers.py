from rest_framework import serializers

from apps.catalog.serializers import ProductForCatalogSerializer
from apps.main.models import Company, Brand


class CompanySerializer(serializers.ModelSerializer):
    """
    Сериализатор компании
    """

    class Meta:
        model = Company
        fields = [
            'uuid',
            'name',
            'description',
        ]


class BrandForProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор отображение брэнда у товара на страничке
    """

    class Meta:
        model = Brand
        fields = [
            'uuid',
            'name',
        ]


class BrandWithProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор отображение брэнда у товара на страничке
    """

    image = serializers.ImageField()
    products = ProductForCatalogSerializer(many=True)

    class Meta:
        model = Brand
        fields = [
            'uuid',
            'name',
            'description',
            'image',
            'products',
        ]


class BrandSerializer(serializers.ModelSerializer):
    """
    Сериализатор отображение брэндов на главной странице
    """

    image = serializers.ImageField()

    class Meta:
        model = Brand
        fields = [
            'uuid',
            'name',
            'image',
        ]
