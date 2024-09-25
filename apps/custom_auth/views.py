import asyncio
from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from apps.custom_auth.serializers import (
    ContactSerializer,
    ContactInfoSerializer,
    VerifyOTPSerializer,
    PasswordSerializer,
    ChangePasswordSerializer,
)
from apps.custom_auth.services.code import send_verification_code
from apps.custom_auth.services.contact import ContactService
from apps.users.services.session import SessionService


@extend_schema(
    request=ContactSerializer,
    responses=ContactInfoSerializer,
    description='Отправка кода верификации на телефон или почту',
    summary='Отправка кода верификации на телефон или почту',
    tags=['Авторизация'],
)
@api_view(['POST'])
def send_code_handler(request: Request) -> Response:
    """
    Функция для отправки кода на телефон или почту
    """
    serializer_response = ContactSerializer(data=request.data)
    serializer_response.is_valid(raise_exception=True)
    contact_info = serializer_response.validated_data['contact']
    info = ContactService.check_contact_type(contact_info)

    serializer = ContactInfoSerializer(info)
    result = asyncio.run(send_verification_code(serializer.data))
    return Response({'data': result}, status=status.HTTP_200_OK)


@extend_schema(
    request=VerifyOTPSerializer,
    responses=VerifyOTPSerializer,
    description='Проверка введенного кода верификации',
    summary='Проверка введенного кода верификации',
    tags=['Авторизация'],
)
@api_view(['POST'])
def verify_code_handler(request: Request, **kwargs: Any) -> Response:
    """
    Функция для проверки кода подтверждения
    """
    serializer = VerifyOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    tokens = serializer.save()
    SessionService.create(request, serializer.validated_data['user'])
    return Response({'data': tokens}, status=status.HTTP_200_OK)


@extend_schema(
    request=PasswordSerializer,
    responses=PasswordSerializer,
    description='Авторизация через пароль',
    summary='Авторизация через пароль',
    tags=['Авторизация'],
)
@api_view(['POST'])
def login_password_handler(request: Request) -> Response:
    """
    Функция для входа пользователя через пароль
    """
    serializer = PasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data.get('user')
    if not user:
        return Response(
            {
                'error': {
                    'code': status.HTTP_401_UNAUTHORIZED,
                    'message': 'Authentication failed',
                }
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
    contact_info = serializer.validated_data['contact']
    password = serializer.validated_data['password']
    info = ContactService.check_contact_type(contact_info)

    serializer = ContactInfoSerializer(info)
    result = asyncio.run(send_verification_code(serializer.data, password))
    return Response({'data': result}, status=status.HTTP_200_OK)


@extend_schema(
    request=ChangePasswordSerializer,
    responses=ChangePasswordSerializer,
    description='Смена пароля через код подтверждения',
    summary='Смена пароля через код подтверждения',
    tags=['Авторизация'],
)
@api_view(['POST'])
def change_password_handler(request: Request) -> Response:
    """
    Обработчик для смены пароля через код подтверждения
    """
    serializer = ChangePasswordSerializer(
        data=request.data, context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    tokens = serializer.save()
    return Response(tokens, status=status.HTTP_200_OK)
