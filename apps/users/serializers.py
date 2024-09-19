from rest_framework import serializers

from apps.users.models import User


class AuthUserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = [
            'uuid',
            'email',
            'firstName',
            'lastName',
            'phoneNumber',
            'is_staff',
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
