import uuid as py_uuid

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.catalog.serializers import (
    MainCategorySerializer,
    SubCategorySerializer,
    ProductVarietySerializer,
    ProductTypeSerializer,
    ProductSubtypeSerializer,
)
from apps.catalog.services.catalog import (
    get_main_category,
    get_sub_category,
    get_product_variety,
    get_product_type,
    get_product_subtype,
    get_all_categories,
)

CATEGORY_TYPES = {
    'main': (get_main_category, MainCategorySerializer),
    'sub': (get_sub_category, SubCategorySerializer),
    'variety': (get_product_variety, ProductVarietySerializer),
    'type': (get_product_type, ProductTypeSerializer),
    'subtype': (get_product_subtype, ProductSubtypeSerializer),
}


@extend_schema(
    responses=MainCategorySerializer,  # Указываем тип ответа
    description='Получение каталога товаров',
    summary='Получение каталога товаров',
    tags=['Каталог'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_category_handler(
    request: Request, uuid: py_uuid.uuid4, slug: str
) -> Response:
    """
    Обработчик на получение категорий
    """
    category_type = request.query_params.get('type')

    if not category_type or category_type not in CATEGORY_TYPES:
        return Response(
            {'error': 'Invalid or missing category type'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    get_category_function, serializer_class = CATEGORY_TYPES[category_type]

    catalog = get_category_function(uuid, slug)
    serializer = serializer_class(catalog)

    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@extend_schema(
    responses=MainCategorySerializer(many=True),
    description='Получение конкретной категории по UUID и slug',
    summary='Получение конкретной категории по UUID и slug',
    tags=['Каталог'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_catalog_handler(request: Request) -> Response:
    """
    Обработчик на получение каталога
    """
    categories = get_all_categories()
    serializer = MainCategorySerializer(categories, many=True)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)
