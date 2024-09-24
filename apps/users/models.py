import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from apps.main.models import Company
from apps.models import BaseModel

ROLES = (
    ('admin', 'Администратор'),
    ('company', 'Компания'),
)


class UserManager(BaseUserManager):
    """
    Менеджер пользователей, который наследуется от BaseUserManager.
    Обеспечивает создание пользователей и суперпользователей.
    """

    def create_user(
        self,
        email: str,
        firstName: str,
        lastName: str,
        phoneNumber: str,
        password: str | None = None,
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
        email: str,
        firstName: str,
        lastName: str,
        phoneNumber: str,
        password: str | None = None,
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
    """
    Модель прав
    """

    name = models.CharField(max_length=250)
    codename = models.CharField(max_length=250)
    role = models.CharField(max_length=255, choices=ROLES)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Права'
        verbose_name_plural = 'Права'


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Модель пользователя
    """

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
    avatar = models.ImageField(
        upload_to='avatars/', null=True, blank=True, verbose_name='Фото'
    )
    isStaff = models.BooleanField(default=False, verbose_name='Администратор?')
    isCompany = models.BooleanField(default=False, verbose_name='Компания?')
    approvedPhone = models.BooleanField(
        default=False, verbose_name='Подтвержден номер телефона?'
    )
    approvedEmail = models.BooleanField(
        default=False, verbose_name='Подтверждена почта?'
    )
    dateOfBirth = models.DateField(
        null=True, blank=True, verbose_name='Дата рождения'
    )
    address = models.TextField(null=True, blank=True, verbose_name='Адрес')
    secretKey = models.CharField(max_length=32, null=True, blank=True)
    language = models.CharField(
        max_length=10,
        choices=[('en', 'English'), ('ru', 'Russian')],
        default='ru',
        verbose_name='Язык',
    )

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Компания',
    )
    permissions = models.ManyToManyField(
        Permission, verbose_name='Права', blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'phoneNumber']

    objects = UserManager()

    def __str__(self) -> str:
        if self.email:
            return self.email
        elif self.phoneNumber:
            return str(self.phoneNumber)
        elif self.firstName or self.lastName:
            return f"{self.firstName or ''} {self.lastName or ''}".strip()
        else:
            return str(self.uuid)

    @property
    def username(self) -> str:
        return f'{self.firstName} {self.lastName}'

    @property
    def is_staff(self) -> bool:
        return self.isStaff

    def clean(self) -> None:
        if self.isStaff and self.isCompany:
            raise ValidationError(
                'Пользователь не может быть администратором и '
                'компанией одновременно'
            )

    def has_perms_by_codename(self, codename: str) -> bool:
        """
        Проверяет, есть ли у пользователя конкретное разрешение по его коду
        """
        permission = Permission.objects.filter(codename=codename).first()
        if permission:
            return self.permissions.filter(pk=permission.pk).exists()
        return False

    def get_absolute_url(self) -> str:
        return reverse('admin:users_user_change', args=[str(self.id)])

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserSession(BaseModel):
    """
    Модель сеанса пользователя
    """

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
    userAgent = models.CharField(max_length=255, verbose_name='User Agent')

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sessions'
    )

    def __str__(self) -> str:
        return f'{self.user.email} - {self.deviceType} ({self.ip})'

    class Meta:
        verbose_name = 'Сеанс пользователя'
        verbose_name_plural = 'Сеансы пользователей'
