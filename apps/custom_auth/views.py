from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from apps.custom_auth.serializers import (
    VerifyOTPSerializer,
    ContactSerializer,
    ChangePasswordSerializer,
)
from apps.custom_auth.services.email import send_email_verification
from apps.custom_auth.services.sms import generate_otp, send_sms
from apps.users.services.user import UserService
from config.settings import API_ID


@api_view(['POST'])
def send_code_handler(request: Request) -> Response:
    """
    Функция для отправки кода на телефон или почту.
    """
    serializer = ContactSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    contact_info = serializer.validated_data['contact']

    otp_code, secret = generate_otp()
    message = f'Ваш код подтверждения: {otp_code}'

    if contact_info['type'] == 'phone':
        phone_number = contact_info['value']
        UserService.get_or_create_with_phone_number(phone_number, secret)
        result = send_sms(API_ID, phone_number, message)
    elif contact_info['type'] == 'email':
        email = contact_info['value']
        UserService.get_or_create_with_email(email, secret)
        result = send_email_verification(email, message)
    else:
        return Response(
            {'detail': 'Неподдерживаемый тип данных.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

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
def change_password_handler(request):
    """
    Обработчик для смены пароля через код подтверждения.
    """
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    result = serializer.save()
    return Response({'data': result}, status=status.HTTP_200_OK)
