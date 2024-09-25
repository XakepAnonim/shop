from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.models import User
from apps.users.services.session import SessionService


def create_user(
    request: Request,
    backend: str,
    response: Response,
    *args: Any,
    **kwargs: Any,
) -> None:
    """
    Создание пользователя при авторизации через Google
    """
    email: str | None = response.get('email')
    first_name: str | None = response.get('given_name')
    last_name: str | None = response.get('family_name')
    avatar: str | None = response.get('picture')
    approved_email: str | None = response.get('email_verified')

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
