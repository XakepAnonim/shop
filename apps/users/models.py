from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from apps.models import BaseModel
import uuid

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
        verbose_name='Email address',
        blank=True,
        null=True,
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='First Name',
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Last Name',
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name='Phone Number',
        unique=True,
        blank=True,
        null=True,
    )
    is_staff = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    date_of_birth = models.DateField(
        null=True, blank=True, verbose_name='Date of Birth'
    )
    avatar = models.ImageField(
        upload_to='avatars/', null=True, blank=True, verbose_name='Avatar'
    )
    address = models.TextField(null=True, blank=True, verbose_name='Address')
    company_name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='Company Name'
    )
    secret_key = models.CharField(max_length=32, null=True, blank=True)
    approved_phone = models.BooleanField(
        default=False, verbose_name='Approved Phone'
    )
    approved_email = models.BooleanField(
        default=False, verbose_name='Approved Email'
    )
    language = models.CharField(
        max_length=10,
        choices=[('en', 'English'), ('ru', 'Russian')],
        default='ru',
    )

    permissions = models.ManyToManyField(
        Permission, verbose_name='Права', blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = UserManager()

    def clean(self):
        if self.is_admin and self.is_company:
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
