import asyncio
import re

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from apps.custom_auth.serializers import (
    VerifyOTPSerializer,
    ContactSerializer,
    PasswordSerializer,
    ChangePasswordSerializer,
    ContactInfoSerializer,
)
from apps.custom_auth.services.code import send_verification_code


@api_view(['POST'])
def send_code_handler(request: Request) -> Response:
    """
    Функция для отправки кода на телефон или почту.
    """
    serializer_response = ContactSerializer(data=request.data)
    serializer_response.is_valid(raise_exception=True)
    contact_info = serializer_response.validated_data['contact']

    if re.match(r'^\+?7\d{10}$', contact_info):
        info = {'type': 'phone', 'value': contact_info}
    elif re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', contact_info):
        info = {'type': 'email', 'value': contact_info}

    serializer = ContactInfoSerializer(info)
    result = asyncio.run(send_verification_code(serializer.data))
    return Response({'data': result}, status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_code_handler(request: Request) -> Response:
    """
    Функция для проверки кода подтверждения.
    """
    serializer = VerifyOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    tokens = serializer.save()
    return Response({'data': tokens}, status=status.HTTP_200_OK)


@api_view(['POST'])
def login_password_handler(request: Request) -> Response:
    """
    Функция для входа пользователя через пароль.
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

    if re.match(r'^\+?7\d{10}$', contact_info):
        info = {'type': 'phone', 'value': contact_info}
    elif re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', contact_info):
        info = {'type': 'email', 'value': contact_info}

    serializer = ContactInfoSerializer(info)
    result = asyncio.run(send_verification_code(serializer.data, password))
    return Response({'data': result}, status=status.HTTP_200_OK)


@api_view(['POST'])
def change_password_handler(request: Request) -> Response:
    """
    Обработчик для смены пароля через код подтверждения.
    """
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    tokens = serializer.save()
    return Response(tokens, status=status.HTTP_200_OK)


@api_view(['POST'])
def reset_password_handler(request: Request) -> Response:
    pass
