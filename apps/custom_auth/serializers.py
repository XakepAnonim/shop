import re

from django.contrib.auth import authenticate
from pyotp import TOTP
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.custom_auth.services.contact import ContactService


class VerifyOTPSerializer(serializers.Serializer):
    """
    Сериализатор верификации кода
    """

    contact = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, data: dict) -> dict:
        """
        Валидация данных и проверка кода подтверждения.
        """
        contact = data.get('contact')
        code = data.get('code')
        user = ContactService.check_contact_info(contact)

        totp = TOTP(user.secretKey, interval=600)
        if not totp.verify(code):
            raise serializers.ValidationError(
                {'data': 'Неверный код подтверждения'}
            )
        data['user'] = user
        return data

    def create(self, validated_data: dict) -> dict:
        """
        Генерация JWT токенов для пользователя.
        """
        user = validated_data['user']
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', validated_data['contact']):
            user.approved_email = True
        elif re.match(r'^\+?7\d{10}$', validated_data['contact']):
            user.approved_phone = True
        else:
            raise serializers.ValidationError(
                'E-mail/ телефон или пароль указаны неверно.'
            )
        user.save()

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class ContactSerializer(serializers.Serializer):
    """
    Сериализатор контакта
    """

    contact = serializers.CharField()


class ContactInfoSerializer(serializers.Serializer):
    """
    Сериализатор значений контакта
    """

    type = serializers.CharField()
    value = serializers.CharField()


class PasswordSerializer(serializers.Serializer):
    """
    Сериализатор авторизации через пароль
    """

    contact = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=16)

    def validate(self, attrs: dict) -> dict:
        """
        Проверка входных данных и аутентификация пользователя.
        """
        contact = attrs.get('contact')
        password = attrs.get('password')

        phone_number = None
        email = None
        user = None

        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', contact):
            email = contact
        elif re.match(r'^\+?7\d{10}$', contact):
            phone_number = contact
        else:
            raise serializers.ValidationError(
                'E-mail/ телефон или пароль указаны неверно.'
            )

        if phone_number:
            user = authenticate(phone_number=phone_number, password=password)
        elif email:
            user = authenticate(email=email, password=password)

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """
    Сериализатор смены пароля
    """

    contact = serializers.CharField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8, max_length=16)

    def validate(self, data: dict) -> dict:
        """
        Валидация данных: проверка кода подтверждения и существования пользователя.
        """
        contact = data.get('contact')
        code = data.get('code')
        user = ContactService.check_contact_info(contact)

        totp = TOTP(user.secretKey, interval=600)
        if not totp.verify(code):
            raise serializers.ValidationError(
                {'data': 'Неверный код подтверждения'}
            )
        data['user'] = user
        return data

    def save(self) -> dict:
        """
        Обновление пароля пользователя.
        """
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
