import pyotp
from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.response import Response

from apps.custom_auth.services.email import send_email_verification
from apps.custom_auth.services.sms import send_sms
from apps.users.services.user import UserService


def generate_otp():
    """
    Генерация кода и его секретного ключа.
    """
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=600)
    otp_code = totp.now()
    print('Generated code: ' + otp_code)
    print('Generated key: ' + secret)
    return otp_code, secret


async def send_verification_code(contact_info, password=None):
    otp_code, secret = generate_otp()
    message = f'Ваш код подтверждения: {otp_code}'

    if contact_info['type'] == 'phone':
        await sync_to_async(UserService.get_or_create_user)(
            contact_info, secret, password
        )
        return await send_sms(contact_info['value'], message)
    elif contact_info['type'] == 'email':
        await sync_to_async(UserService.get_or_create_user)(
            contact_info, secret, password
        )
        return send_email_verification(contact_info['value'], message)
    else:
        return Response(
            {'detail': 'Неподдерживаемый тип данных.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
