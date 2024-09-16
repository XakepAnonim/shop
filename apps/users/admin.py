from django.contrib import admin

from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'is_staff',
        'is_company',
        'company',
        'approved_phone',
        'approved_email',
    )
    list_filter = (
        'is_staff',
        'is_company',
        'approved_phone',
        'approved_email',
        'language',
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'phone_number',
                    'password',
                    'is_staff',
                    'is_company',
                )
            },
        ),
        ('Important dates', {'fields': ('updated_at', 'created_at')}),
        (
            'Additional Info',
            {
                'fields': (
                    'date_of_birth',
                    'avatar',
                    'address',
                    'company_name',
                    'approved_phone',
                    'approved_email',
                    'language',
                )
            },
        ),
    )
