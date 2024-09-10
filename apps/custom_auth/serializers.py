import re

from pyotp import TOTP
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.services.user import UserService


class VerifyOTPSerializer(serializers.Serializer):
    contact = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        """
        Валидация данных и проверка кода подтверждения.
        """
        contact = data.get('contact')
        code = data.get('code')

        if '@' in contact:
            user = UserService.get_by_email(contact)
            if not user:
                raise serializers.ValidationError(
                    'Пользователь с таким email не найден.'
                )
        else:
            user = UserService.get_by_phone_number(contact)
            if not user:
                raise serializers.ValidationError(
                    'Пользователь с таким номером телефона не найден.'
                )

        TOTP(user.secret_key, interval=300)
        data['user'] = user
        return data

    def create(self, validated_data):
        """
        Генерация JWT токенов для пользователя.
        """
        user = validated_data['user']
        if '@' in validated_data['contact']:
            user.approved_email = True
        else:
            user.approved_phone = True
        user.save()

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class ContactSerializer(serializers.Serializer):
    contact = serializers.CharField()

    def validate(self, value):
        """
        Проверяем, что введены либо телефон, либо email.
        """
        if re.match(r'^\+?7\d{10}$', value):
            return {'type': 'phone', 'value': value}
        elif re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            return {'type': 'email', 'value': value}
        else:
            raise serializers.ValidationError(
                'Введите корректный номер телефона или email.'
            )


class PasswordSerializer(serializers.Serializer):
    contact = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=16)

    def validate(self, value):
        """
        Проверяем, что введены либо телефон, либо email.
        """
        if re.match(r'^\+?7\d{10}$', value):
            return {'type': 'phone', 'value': value}
        elif re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            return {'type': 'email', 'value': value}
        else:
            raise serializers.ValidationError(
                'Введите корректный номер телефона или email.'
            )


class ChangePasswordSerializer(serializers.Serializer):
    contact = serializers.CharField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8, max_length=16)

    def validate(self, data):
        """
        Валидация данных: проверка кода подтверждения и существования пользователя.
        """
        contact = data.get('contact')
        code = data.get('code')

        if '@' in contact:
            user = UserService.get_by_email(contact)
            if not user:
                raise serializers.ValidationError(
                    'Пользователь с таким email не найден.'
                )
        else:
            user = UserService.get_by_phone_number(contact)
            if not user:
                raise serializers.ValidationError(
                    'Пользователь с таким номером телефона не найден.'
                )

        TOTP(user.secret_key, interval=300)
        data['user'] = user
        return data

    def save(self, validated_data):
        """
        Обновление пароля пользователя.
        """
        user = validated_data['user']
        new_password = validated_data['new_password']
        user.set_password(new_password)
        user.save()
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
