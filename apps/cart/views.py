from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.cart.serializers import CartSerializer
from apps.cart.services.cart import CartService
from apps.products.services.product import ProductService


@extend_schema(
    responses=CartSerializer,
    description='Получение корзины пользователя',
    summary='Получение корзины пользователя',
    tags=['Корзина'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart_handler(request: Request) -> Response:
    """
    Обработчик получения корзины
    """
    user = request.user
    cart = CartService.get(user)
    serializer = CartSerializer(cart)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@extend_schema(
    responses=CartSerializer,
    description='Добавление товара в корзину пользователя',
    summary='Добавление товара в корзину пользователя',
    tags=['Корзина'],
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart_handler(request: Request, uuid: str, slug: str) -> Response:
    """
    Обработчик добавления товара в корзину
    """
    user = request.user
    product = ProductService.get(uuid, slug)
    quantity = request.data.get('quantity', 1)
    try:
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError
    except (ValueError, TypeError):
        return Response(
            {'error': 'Некорректное количество'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    cart = CartService.add_product(user, product, quantity)
    serializer = CartSerializer(cart)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@extend_schema(
    responses=CartSerializer,
    description='Удаление или уменьшение количества товара в корзине пользователя',
    summary='Удаление или уменьшение количества товара в корзине пользователя',
    tags=['Корзина'],
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart_handler(
    request: Request, uuid: str, slug: str
) -> Response:
    """
    Обработчик удаления или уменьшения количества товара в корзине
    """
    user = request.user
    product = ProductService.get(uuid, slug)
    quantity = request.data.get('quantity', 1)
    try:
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError
    except (ValueError, TypeError):
        return Response(
            {'error': 'Некорректное количество'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    cart = CartService.remove_product(user, product, quantity)
    serializer = CartSerializer(cart)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)
