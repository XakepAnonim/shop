import re

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.users.models import User
from apps.users.services.user import UserService


class Contact:
    @staticmethod
    def check_contact_type(contact) -> dict | Response:
        """
        Проверка на тип контакта (телефон или почта)
        """
        if re.match(r'^\+?7\d{10}$', contact):
            info = {'type': 'phone', 'value': contact}
        elif re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', contact):
            info = {'type': 'email', 'value': contact}
        else:
            raise ValidationError('E-mail/ телефон указаны неверно')
        return info

    @staticmethod
    def check_contact_info(contact, serializers) -> User:
        """
        Получение пользователя по контакту (почта или телефон)
        """
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', contact):
            user = UserService.get_by_email(contact)
            if not user:
                raise serializers.ValidationError(
                    'Пользователь с таким email не найден.'
                )
        elif re.match(r'^\+?7\d{10}$', contact):
            user = UserService.get_by_phone_number(contact)
            if not user:
                raise serializers.ValidationError(
                    'Пользователь с таким номером телефона не найден.'
                )
        else:
            raise serializers.ValidationError(
                'E-mail/ телефон указаны неверно'
            )
        return user
