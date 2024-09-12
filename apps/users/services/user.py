import uuid

from django.shortcuts import get_object_or_404

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
    def get_or_create_user(contact, secret, password=None):
        """
        Получает или создаёт пользователя на основе контактной информации.
        """
        if contact['type'] == 'phone':
            user, created = User.objects.get_or_create(
                phone_number=contact['value']
            )
        elif contact['type'] == 'email':
            user, created = User.objects.get_or_create(email=contact['value'])
        user.secret_key = secret
        if created and password:
            user.set_password(password)
        user.save()
        return user

    @staticmethod
    def get_or_create_user_google(backend, user, response, *args, **kwargs):
        """
        Функция для получения или создания пользователя на основе данных от Google.
        """
        print(f"Получены данные от Google: {response}")
        email = response.get('email')
        first_name = response.get('given_name')
        last_name = response.get('family_name')
        picture = response.get('picture')
        locale = response.get('locale')

        try:
            user = User.objects.get(email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except User.DoesNotExist:
            user = User.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                avatar=picture,
                language=locale,
                approved_email=response.get('verified_email', False),
            )
            user.set_unusable_password()
            user.save()
        return user
