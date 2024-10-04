from django.contrib import admin
from django.urls.base import reverse
from django.utils.html import format_html

from apps.cart.models import CartItem, Cart, Order


class CartItemInline(admin.TabularInline):
    """
    Инлайн для отображения элементов корзины в админке Cart.
    """

    model = CartItem
    extra = 1
    readonly_fields = (
        'uuid',
        'price',
        'total',
    )
    fields = ('uuid', 'product', 'quantity', 'price', 'total')
    can_delete = True

    @admin.display(description='Цена за единицу')
    def price(self, obj):
        return obj.product.price if obj.product else '-'

    @admin.display(description='Итого')
    def total(self, obj):
        if obj.product and obj.quantity:
            return obj.product.price * obj.quantity
        return '-'

    @admin.display(description='UUID')
    def uuid_display(self, obj):
        return obj.uuid


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'user_display', 'total_price')
    search_fields = ('user__email',)
    readonly_fields = ('uuid', 'total_price')
    inlines = [CartItemInline]

    @admin.display(description='Пользователь')
    def user_display(self, obj: Cart) -> str:
        url = reverse('admin:users_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'owner_display',
        'quantity',
        'totalPrice',
        'deliveryType',
        'paymentMethod',
        'onlineMethod',
        'deliveryAddress',
        'status',
    )
    search_fields = ('user',)
    list_filter = ('status', 'paymentMethod', 'deliveryType', 'onlineMethod')
    readonly_fields = (
        'uuid',
        'totalPrice',
        'quantity',
        'deliveryType',
        'paymentMethod',
        'onlineMethod',
        'deliveryAddress',
    )

    @admin.display(description='Чей')
    def owner_display(self, obj: Order) -> str:
        if obj.user:
            url = reverse('admin:users_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username) if obj.user else '-'
        elif obj.company:
            url = reverse('admin:main_company_change', args=[obj.company.id])
            return format_html('<a href="{}">{}</a>', url, obj.company.name) if obj.company else '-'
