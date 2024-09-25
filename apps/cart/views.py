from typing import cast

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.cart.serializers import CartSerializer
from apps.cart.services.cart import CartService
from apps.products.services.product import ProductService
from apps.users.models import User


@extend_schema(
    responses=CartSerializer,
    description='Получение корзины пользователя',
    summary='Получение корзины пользователя',
    tags=['Корзина'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart_handler(request: Request) -> Response:
    user = cast(User, request.user)
    cart = CartService.get(user)
    serializer = CartSerializer(cart)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@extend_schema(
    responses=CartSerializer,
    description='Добавление товара в корзину пользователя',
    summary='Добавление товара в корзину пользователя',
    tags=['Корзина'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_cart_handler(request: Request, uuid: str, slug: str) -> Response:
    user = cast(User, request.user)
    product = ProductService.get(uuid, slug)
    cart = CartService.get_or_create(user, product)
    serializer = CartSerializer(cart)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


# так же нужно сделать запрос на увеличение кол-ва самого товара в корзине
