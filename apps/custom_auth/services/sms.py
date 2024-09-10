from urllib.error import URLError
from urllib.parse import quote
from urllib.request import urlopen

import pyotp


def generate_otp():
    """
    Генерация кода для SMS и его секретного ключа.
    """
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=300)
    otp_code = totp.now()
    print('Generated code: ' + otp_code)
    print('Generated key: ' + secret)
    return otp_code, secret


def send_sms(api_id, phone_number, message):
    """
    Функция для отправки SMS через sms.ru.
    """
    url = f'https://sms.ru/sms/send?api_id={api_id}&to={phone_number}&msg={quote(message)}&json=1'
    try:
        res = urlopen(url, timeout=10)
        service_result = res.read().decode('utf-8')
        if '"status":"OK"' in service_result:
            return {'SMS отправлено успешно.'}
        else:
            return {f'Ошибка отправки SMS: {service_result}'}
    except URLError as e:
        return {'Ошибка при отправке запроса:', e}

