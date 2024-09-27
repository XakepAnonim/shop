from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.catalog.serializers import CategorySerializer
from apps.catalog.services.catalog import get_category, get_all_categories


@extend_schema(
    responses=CategorySerializer,
    description='Получение конкретной категории по UUID и slug',
    summary='Получение конкретной категории по UUID и slug',
    tags=['Каталог'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_category_handler(request: Request, uuid: str, slug: str) -> Response:
    """
    Обработчик на получение конкретной категории по uuid и slug.
    """
    # cache_key = f'category_{uuid}_{slug}'
    # cached_category = cache.get(cache_key)
    #
    # if cached_category:
    #     return Response({'data': cached_category}, status=status.HTTP_200_OK)

    category = get_category(uuid, slug)
    serializer = CategorySerializer(category)

    # # Кэшируем результат на 10 минут
    # cache.set(cache_key, serializer.data, timeout=600)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@extend_schema(
    responses=CategorySerializer(many=True),
    description='Получение всего каталога',
    summary='Получение всего каталога',
    tags=['Каталог'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_catalog_handler(request: Request) -> Response:
    """
    Обработчик на получение всего каталога.
    """
    categories = get_all_categories()
    serializer = CategorySerializer(categories, many=True)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)
