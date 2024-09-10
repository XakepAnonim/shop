from django.shortcuts import get_object_or_404
import uuid

from apps.users.models import User


class UserService:
    @staticmethod
    def get(uuid: uuid) -> User:
        user = get_object_or_404(User, uuid=uuid)
        return user

    @staticmethod
    def get_by_phone_number(phone_number: int) -> User:
        user = get_object_or_404(User, phone_number=phone_number)
        return user

    @staticmethod
    def get_by_email(email: int) -> User:
        user = get_object_or_404(User, email=email)
        return user

    @staticmethod
    def get_or_create_with_phone_number(phone_number, secret):
        user, created = User.objects.get_or_create(phone_number=phone_number)
        user.secret_key = secret
        user.save()
        return user

    @staticmethod
    def get_or_create_with_email(email, secret):
        user, created = User.objects.get_or_create(email=email)
        user.secret_key = secret
        user.save()
        return user
