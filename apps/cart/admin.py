from django.contrib import admin
from django.utils.html import format_html

from apps.cart.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'count', 'total_price', 'user_display')
    search_fields = ('user',)

    @admin.display(description='Пользователь')
    def user_display(self, obj: Cart) -> str:
        return format_html(
            '<a href="{}">{}</a>',
            obj.user.get_absolute_url(),
            obj.user,
        )
