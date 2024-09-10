from rest_framework import serializers

from apps.users.models import User


class AuthUserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = [
            'uuid',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'is_staff',
            'date_of_birth',
            'avatar',
            'address',
            'company_name',
            'approved_phone',
            'approved_email',
            'language',
            'permissions',
        ]
        read_only_fields = ('uuid', 'approved_phone', 'approved_email')


class UpdateUserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = [
            'uuid',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'date_of_birth',
            'avatar',
            'address',
            'company_name',
            'language',
        ]


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=15, label='Введите номер телефона'
    )
