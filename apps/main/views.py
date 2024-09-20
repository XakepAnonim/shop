from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.main.models import Brand
from apps.main.serializers import BrandSerializer


@extend_schema(
    responses=BrandSerializer,
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
    brand = get_object_or_404(Brand, name=name)
    serializer = BrandSerializer(brand)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)
