from rest_framework import serializers

from apps.catalog.serializers import ProductForCatalogSerializer
from apps.main.models import Brand, Company


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


class BrandSerializer(serializers.ModelSerializer):
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
