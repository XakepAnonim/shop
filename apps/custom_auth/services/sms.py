import smsaero

from config.settings import SMSAERO_EMAIL, SMSAERO_API_KEY


async def send_sms(phone: int, message: str) -> None:
    """
    Функция для Отправки sms на номер телефона.
    """
    phone_number = int(phone.replace("+", ""))
    api = smsaero.SmsAero(SMSAERO_EMAIL, SMSAERO_API_KEY)
    try:
        await api.send_sms(phone_number, message)
    finally:
        await api.close_session()
