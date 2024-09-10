import pyotp
from rest_framework import status
from rest_framework.response import Response

from apps.custom_auth.services.email import send_email_verification
from apps.custom_auth.services.sms import send_sms
from apps.users.services.user import UserService
from config.settings import API_ID


def generate_otp():
    """
    Генерация кода и его секретного ключа.
    """
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=300)
    otp_code = totp.now()
    print('Generated code: ' + otp_code)
    print('Generated key: ' + secret)
    return otp_code, secret


def send_verification_code(contact_info, password=None):
    otp_code, secret = generate_otp()
    message = f'Ваш код подтверждения: {otp_code}'

    if contact_info['type'] == 'phone':
        UserService.get_or_create_user(contact_info, secret, password)
        return send_sms(API_ID, contact_info['value'], message)
    elif contact_info['type'] == 'email':
        UserService.get_or_create_user(contact_info, secret, password)
        return send_email_verification(contact_info['value'], message)
    else:
        return Response(
            {'detail': 'Неподдерживаемый тип данных.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
