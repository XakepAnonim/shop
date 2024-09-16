import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.main.models import Company
from apps.models import BaseModel

ROLES = (
    ('admin', 'Администратор'),
    ('company', 'Компания'),
)


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        first_name,
        last_name,
        phone_number,
        password=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        first_name,
        last_name,
        phone_number,
        password=None,
        **extra_fields,
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(
            email,
            first_name,
            last_name,
            phone_number,
            password,
            **extra_fields,
        )


class Permission(models.Model):
    name = models.CharField(max_length=250)
    codename = models.CharField(max_length=250)
    role = models.CharField(max_length=255, choices=ROLES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Права'
        verbose_name_plural = 'Права'


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'
    )
    email = models.EmailField(
        unique=True,
        max_length=255,
        verbose_name='Почта',
        blank=True,
        null=True,
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя',
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия',
        blank=True,
        null=True,
    )
    phone_number = PhoneNumberField(
        max_length=15,
        verbose_name='Номер телефона',
        unique=True,
        blank=True,
        null=True,
    )
    is_staff = models.BooleanField(
        default=False, verbose_name='Администратор?'
    )
    is_company = models.BooleanField(default=False, verbose_name='Компания?')
    date_of_birth = models.DateField(
        null=True, blank=True, verbose_name='Дата рождения'
    )
    avatar = models.ImageField(
        upload_to='avatars/', null=True, blank=True, verbose_name='Фото'
    )
    address = models.TextField(null=True, blank=True, verbose_name='Адрес')
    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Компания',
    )
    secret_key = models.CharField(max_length=32, null=True, blank=True)
    approved_phone = models.BooleanField(
        default=False, verbose_name='Подтвержден номер телефона?'
    )
    approved_email = models.BooleanField(
        default=False, verbose_name='Подтверждена почта?'
    )
    language = models.CharField(
        max_length=10,
        choices=[('en', 'English'), ('ru', 'Russian')],
        default='ru',
        verbose_name='Язык',
    )

    permissions = models.ManyToManyField(
        Permission, verbose_name='Права', blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return ''

    def clean(self):
        if self.is_staff and self.is_company:
            raise ValidationError(
                'Пользователь не может быть администратором и '
                'компанией одновременно'
            )

    def has_perms(self, codename):
        """
        Проверяет, есть ли у пользователя конкретное разрешение по его коду
        """
        permission = Permission.objects.filter(codename=codename).first()
        if permission:
            return self.permissions.filter(pk=permission.pk).exists()
        return False

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
