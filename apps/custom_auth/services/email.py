from django.core.mail import send_mail

from config import settings


def send_email_verification(email, message):
    """
    Отправка email с кодом подтверждения.
    """
    subject = 'Код подтверждения'
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        return {'status': 'OK', 'message': 'Email отправлен успешно.'}
    except Exception as e:
        return {
            'status': 'ERROR',
            'message': f'Ошибка при отправке email: {str(e)}',
        }
