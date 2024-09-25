from typing import cast

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.products.serializers import (
    ProductSerializer,
    WishlistProductSerializer,
)
from apps.products.services.product import ProductService
from apps.products.services.wishlist import WishlistService
from apps.users.models import User


@extend_schema(
    responses=ProductSerializer,
    description='Получение товара по UUID и слагу',
    summary='Получение товара по UUID и слагу',
    tags=['Товар'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product(request: Request, uuid: str, slug: str) -> Response:
    """
    Обработчик на получение товара
    """
    product = ProductService.get(uuid, slug)
    serializer = ProductSerializer(product)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@extend_schema(
    responses=WishlistProductSerializer,
    description='Получение желаемых товаров пользователя',
    summary='Получение желаемых товаров пользователя',
    tags=['Избранное'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wishlist_products(request: Request) -> Response:
    """
    Обработчик на получение желаемых товара
    """
    user = cast(User, request.user)
    wishlist = WishlistService.get(user)
    serializer = WishlistProductSerializer(wishlist)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@extend_schema(
    responses=WishlistProductSerializer,
    description='Добавление\убирание товара в избранное',
    summary='Добавление\убирание товара в избранное',
    tags=['Избранное'],
)
@api_view(['GET'])
def post_wishlist_product(request: Request, uuid: str, slug: str) -> Response:
    """
    Обработчик на добавление\убирание товара в избранное
    """
    user = cast(User, request.user)
    product = ProductService.get(uuid, slug)
    wishlist_product = WishlistService.get_or_create(user, product)
    serializer = WishlistProductSerializer(wishlist_product)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)
