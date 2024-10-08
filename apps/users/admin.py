from django.contrib import admin
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import Permission, User, UserSession


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'codename',
        'role',
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'email',
        'firstName',
        'lastName',
        'phoneNumber',
        'isStaff',
        'isCompany',
        'company',
        'approvedPhone',
        'approvedEmail',
    )
    list_filter = (
        'isStaff',
        'isCompany',
        'approvedPhone',
        'approvedEmail',
        'language',
    )
    search_fields = ('email', 'firstName', 'lastName', 'phoneNumber')
    ordering = ('-createdAt',)
    readonly_fields = ('uuid', 'createdAt', 'updatedAt')
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'email',
                    'firstName',
                    'lastName',
                    'phoneNumber',
                    'password',
                    'isStaff',
                    'isCompany',
                )
            },
        ),
        ('Important dates', {'fields': ('updatedAt', 'createdAt')}),
        (
            'Additional Info',
            {
                'fields': (
                    'dateOfBirth',
                    'avatar',
                    'address',
                    'company',
                    'approvedPhone',
                    'approvedEmail',
                    'language',
                )
            },
        ),
    )
    actions = ['generate_jwt_token']

    @admin.display(description='Generate JWT token')
    def generate_jwt_token(self, request: Request, queryset: QuerySet) -> None:
        for user in queryset:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            self.message_user(
                request, f'Token for {user.username}: {access_token}'
            )


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = (
        'authSSID',
        'user',
        'deviceType',
        'deviceName',
        'os',
        'browser',
        'ip',
        'createdAt',
        'isCurrent',
    )
    readonly_fields = (
        'authSSID',
        'user',
        'deviceType',
        'deviceName',
        'os',
        'browser',
        'ip',
        'userAgent',
        'createdAt',
        'country',
        'isCurrent',
    )
