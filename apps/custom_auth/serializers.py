import re

from django.contrib.auth import authenticate
from pyotp import TOTP
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.custom_auth.services.contact import Contact


class VerifyOTPSerializer(serializers.Serializer):
    contact = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        """
        Валидация данных и проверка кода подтверждения.
        """
        contact = data.get('contact')
        code = data.get('code')
        user = Contact.check_contact_info(contact, serializers)

        totp = TOTP(user.secret_key, interval=300)
        if not totp.verify(code):
            raise serializers.ValidationError(
                {'data': 'Неверный код подтверждения'}
            )
        data['user'] = user
        return data

    def create(self, validated_data):
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
    contact = serializers.CharField()


class ContactInfoSerializer(serializers.Serializer):
    type = serializers.CharField()
    value = serializers.CharField()


class PasswordSerializer(serializers.Serializer):
    contact = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=16)

    def validate(self, attrs) -> dict:
        """
        Проверка входных данных и аутентификация пользователя.
        """
        contact = attrs.get('contact')
        password = attrs.get('password')

        phone_number = None
        email = None

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
    contact = serializers.CharField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8, max_length=16)

    def validate(self, data):
        """
        Валидация данных: проверка кода подтверждения и существования пользователя.
        """
        contact = data.get('contact')
        code = data.get('code')
        user = Contact.check_contact_info(contact, serializers)

        totp = TOTP(user.secret_key, interval=300)
        if not totp.verify(code):
            raise serializers.ValidationError(
                {'data': 'Неверный код подтверждения'}
            )
        data['user'] = user
        return data

    def save(self):
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
