import uuid

from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.cart.models import Order
from apps.cart.serializers import CartSerializer, OrderSerializer, OrderDataValidator
from apps.cart.services.cart import CartService
from apps.cart.services.order import OrderService
from apps.cart.services.payment import PaymentService
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
def add_to_cart_handler(request: Request, product_uuid: uuid.uuid4, slug: str) -> Response:
    """
    Обработчик добавления товара в корзину
    """
    product = ProductService.get(product_uuid, slug)
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

    cart = CartService.add_product(request.user, product, quantity)
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
def remove_from_cart_handler(request: Request, product_uuid: uuid.uuid4, slug: str) -> Response:
    """
    Обработчик удаления или уменьшения количества товара в корзине
    """
    product = ProductService.get(product_uuid, slug)
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

    cart = CartService.remove_product(request.user, product, quantity)
    serializer = CartSerializer(cart)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_from_cart_handler(request: Request, product_uuid: uuid.uuid4, slug: str) -> Response:
    """
    Обработчик удаления товара из корзины
    """
    product = ProductService.get(product_uuid, slug)
    cart = CartService.delete_product(request.user, product)
    serializer = CartSerializer(cart)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@transaction.atomic
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_order_handler(request: Request, cart_uuid: uuid.uuid4) -> Response:
    """
    Обработчик подтверждения заказа
    """
    cart = CartService.get_by_uuid(cart_uuid)
    if not cart or cart.items.count() == 0:
        return Response({'error': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)

    # Проверка наличия товара на складе
    OrderService.check_product(cart)

    validator = OrderDataValidator(data=request.data)
    validator.is_valid(raise_exception=True)

    delivery_type: str = validator.validated_data['deliveryType']
    payment_method: str = validator.validated_data['paymentMethod']
    delivery_address: None | str = None
    online_method: None | str = None
    delivery_coordinates: None | list[float, float] = None

    if delivery_type == 'delivery':
        delivery_coordinates = validator.validated_data['deliveryCoordinates']
        delivery_address = validator.validated_data['deliveryAddress']

    if payment_method == 'online':
        online_method = validator.validated_data['onlineMethod']
        order = OrderService.create_order(
            cart, delivery_type, payment_method, delivery_address, online_method, delivery_coordinates, request.user
        )
        try:
            pass
            # PaymentService.process_online_payment(order, request.data.get('paymentData'))
        except Exception as e:
            return Response({'error': 'Ошибка при обработке оплаты: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        order = OrderService.create_order(
            cart, delivery_type, payment_method, delivery_address, online_method, delivery_coordinates, request.user
        )

    CartService.delete(cart)

    serializer = OrderSerializer(order)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)
