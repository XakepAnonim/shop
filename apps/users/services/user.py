import uuid as py_uuid

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from apps.users.models import User


class UserService:
    @staticmethod
    def get(uuid: py_uuid) -> User:
        """
        Получение пользователя по uuid
        """
        user = get_object_or_404(User, uuid=uuid)
        return user

    @staticmethod
    def get_by_phone_number(phone_number: int) -> User:
        """
        Получение пользователя по номеру телефона
        """
        user = get_object_or_404(User, phoneNumber=phone_number)
        return user

    @staticmethod
    def get_by_email(email: int) -> User:
        """
        Получение пользователя по почте
        """
        user = get_object_or_404(User, email=email)
        return user

    @staticmethod
    def get_or_create_user(contact, secret, password=None) -> User:
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

        user.secret_key = secret
        if created and password:
            user.set_password(password)
        user.save()
        return user
