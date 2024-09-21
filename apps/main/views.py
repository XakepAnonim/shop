from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.main.serializers import BrandWithProductSerializer, BrandSerializer
from apps.main.services.brand import BrandService


@extend_schema(
    responses=BrandWithProductSerializer,
    description='Получение информации о бренде и его продуктах по имени',
    summary='Получение информации о бренде и его продуктах по имени',
    tags=['Брэнд'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_brand_handler(request: Request, name: str) -> Response:
    """
    Обработчик на получение брэнда и его товаров
    """
    brand = BrandService.get(name)
    serializer = BrandWithProductSerializer(brand)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@extend_schema(
    responses=BrandSerializer,
    description='Получение информации о брендах',
    summary='Получение информации о брендах',
    tags=['Брэнд'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_brands_handler(request: Request) -> Response:
    """
    Обработчик на получение брэнда и его товаров
    """
    brands = BrandService.get_all()
    serializer = BrandSerializer(brands, many=True)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)
