from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.cart.serializers import CartSerializer
from apps.cart.services.cart import CartService


@extend_schema(
    responses=CartSerializer,
    description='Получение корзины пользователя',
    summary='Получение корзины пользователя',
    tags=['Корзина'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart_handler(request: Request) -> Response:
    cart = CartService.get(request.user)
    serializer = CartSerializer(cart)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)
