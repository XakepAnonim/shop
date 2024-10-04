from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.products.elasticsearch.index import ProductDocument


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cached_search(request: Request) -> Response:
    """
    Поиск товаров по запросу с кэшированием
    """
    query = request.GET.get('q', '')

    if not query:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    cache_key = f'search_{query}'
    result = cache.get(cache_key)

    if not result:
        result = search_products(query)
        cache.set(cache_key, result, timeout=60 * 15)  # кэширование на 15 минут

    return Response({'data': result}, status=status.HTTP_200_OK)


def search_products(query: str):
    cleaned_query = query.replace(',', ' ')

    search = ProductDocument.search().query(
        "multi_match",
        query=cleaned_query,
        fields=['name^3'],
        type="best_fields"
    )
    response = search.execute()

    return [result.to_dict() for result in response]
