import smsaero

from config.settings import SMSAERO_EMAIL, SMSAERO_API_KEY


async def send_sms(phone: str, message: str) -> None:
    """
    Отправка смс на телефон с кодом подтверждения
    """
    phone_number = int(phone.removeprefix('+'))
    api = smsaero.SmsAero(SMSAERO_EMAIL, SMSAERO_API_KEY)
    try:
        await api.send_sms(phone_number, message)
    finally:
        await api.close_session()
