from django.contrib import admin
from django.utils.html import format_html

from apps.main.models import (
    Brand,
    Company,
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_display')
    search_fields = ('name',)
    list_filter = ('company',)

    @admin.display(description='Компания')
    def company_display(self, obj: Brand) -> str:
        return format_html(
            '<a href="{}">{}</a>',
            obj.company.get_absolute_url(),
            obj.company.name,
        )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
