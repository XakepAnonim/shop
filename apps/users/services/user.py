from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from apps.users.models import User


class UserService:
    """
    Сервис для работы с пользователями
    """

    @staticmethod
    def get(uuid: str) -> User:
        """
        Получение пользователя по uuid
        """
        user = get_object_or_404(User, uuid=uuid)
        return user

    @staticmethod
    def get_by_phone_number(phone_number: str) -> User:
        """
        Получение пользователя по номеру телефона
        """
        user = get_object_or_404(User, phoneNumber=phone_number)
        return user

    @staticmethod
    def get_by_email(email: str) -> User:
        """
        Получение пользователя по почте
        """
        user = get_object_or_404(User, email=email)
        return user

    @staticmethod
    def get_or_create_user(
        contact: dict, secret: str, password: str | None = None
    ) -> User:
        """
        Получает или создаёт пользователя на основе контактной информации.
        """
        if contact['type'] == 'phone':
            user, created = User.objects.get_or_create(
                phoneNumber=contact['value']
            )
        elif contact['type'] == 'email':
            user, created = User.objects.get_or_create(email=contact['value'])
        else:
            raise ValidationError('E-mail/ телефон указаны неверно')

        user.secretKey = secret
        if created and password:
            user.set_password(password)
        user.save()
        return user
