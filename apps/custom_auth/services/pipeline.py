from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.services.session import SessionService
from apps.users.models import User


def create_user(
    request: Request, backend: str, response: Response, *args, **kwargs
) -> None:
    """
    Создание пользователя при авторизации через Google
    """
    email = response.get('email')
    first_name = response.get('given_name')
    last_name = response.get('family_name')
    avatar = response.get('picture')
    approved_email = response.get('email_verified')

    user = User.objects.create_user(
        email=email,
        firstName=first_name,
        lastName=last_name,
        avatar=avatar,
        approvedEmail=approved_email,
        phoneNumber=None,
    )
    user.has_usable_password()
    SessionService.create(request, user, **kwargs)
