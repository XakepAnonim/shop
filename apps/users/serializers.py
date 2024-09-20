from rest_framework import serializers

from apps.users.models import User


class AuthUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения профиля пользователя
    """

    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = [
            'uuid',
            'email',
            'firstName',
            'lastName',
            'phoneNumber',
            'isStaff',
            'dateOfBirth',
            'avatar',
            'address',
            'company',
            'approvedPhone',
            'approvedEmail',
            'language',
            'permissions',
        ]
        read_only_fields = ('uuid', 'approvedPhone', 'approvedEmail')


class UpdateUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления профиля пользователя
    """

    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = [
            'uuid',
            'email',
            'firstName',
            'lastName',
            'phoneNumber',
            'dateOfBirth',
            'avatar',
            'address',
            'company',
            'language',
        ]
        read_only_fields = ('uuid',)
