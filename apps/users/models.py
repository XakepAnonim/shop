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
        firstName,
        lastName,
        phoneNumber,
        password=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            firstName=firstName,
            lastName=lastName,
            phoneNumber=phoneNumber,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        firstName,
        lastName,
        phoneNumber,
        password=None,
        **extra_fields,
    ):
        extra_fields.setdefault('isStaff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(
            email,
            firstName,
            lastName,
            phoneNumber,
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
    firstName = models.CharField(
        max_length=50,
        verbose_name='Имя',
        blank=True,
        null=True,
    )
    lastName = models.CharField(
        max_length=50,
        verbose_name='Фамилия',
        blank=True,
        null=True,
    )
    phoneNumber = PhoneNumberField(
        max_length=15,
        verbose_name='Номер телефона',
        unique=True,
        blank=True,
        null=True,
    )
    isStaff = models.BooleanField(default=False, verbose_name='Администратор?')
    isCompany = models.BooleanField(default=False, verbose_name='Компания?')
    dateOfBirth = models.DateField(
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
    secretKey = models.CharField(max_length=32, null=True, blank=True)
    approvedPhone = models.BooleanField(
        default=False, verbose_name='Подтвержден номер телефона?'
    )
    approvedEmail = models.BooleanField(
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
    REQUIRED_FIELDS = ['firstName', 'lastName', 'phoneNumber']

    objects = UserManager()

    def __str__(self):
        if self.email:
            return self.email
        elif self.phoneNumber:
            return str(self.phoneNumber)
        elif self.firstName or self.lastName:
            return f"{self.firstName or ''} {self.lastName or ''}".strip()
        else:
            return str(self.uuid)

    @property
    def username(self):
        return f'{self.firstName} {self.lastName}'

    @property
    def is_staff(self):
        return self.isStaff

    def clean(self):
        if self.isStaff and self.isCompany:
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


class UserSession(BaseModel):
    authSSID = models.CharField(
        max_length=255, unique=True, verbose_name='Auth SSID'
    )
    deviceType = models.CharField(max_length=50, verbose_name='Тип устройства')
    deviceName = models.CharField(
        max_length=255, verbose_name='Имя устройства'
    )
    os = models.CharField(max_length=50, verbose_name='Операционная система')
    browser = models.CharField(max_length=50, verbose_name='Браузер')
    ip = models.CharField(max_length=20, verbose_name='IP-адрес')
    cityName = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(
        max_length=10, verbose_name='Страна', null=True, blank=True
    )
    isCurrent = models.BooleanField(default=True, verbose_name='Активен?')

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sessions'
    )
    userAgent = models.CharField(max_length=255, verbose_name='User Agent')

    def __str__(self):
        return f'{self.user.email} - {self.deviceType} ({self.ip})'

    class Meta:
        verbose_name = 'Сеанс пользователя'
        verbose_name_plural = 'Сеансы пользователей'
