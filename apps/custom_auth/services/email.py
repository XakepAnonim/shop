from django.core.mail import send_mail

from config import settings


def send_email_verification(email, message):
    """
    Отправка email с кодом подтверждения.
    """
    subject = 'Код подтверждения'
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        return {'message': 'Код был отправлен на указанный адрес'}
    except Exception as e:
        return {
            'error': f'Ошибка при отправке email: {str(e)}',
        }
