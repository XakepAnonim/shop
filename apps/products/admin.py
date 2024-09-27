from django.contrib import admin
from django.utils.html import format_html

from apps.products.models import (
    Product,
    CharacteristicGroup,
    Characteristic,
    WishlistProduct,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sku',
        'price',
        'priceCurrency',
        'stockQuantity',
        'isAvailable',
        'brand_display',
    )
    list_filter = ('brand', 'priceCurrency', 'isAvailable')
    search_fields = ('name', 'sku', 'description')
    readonly_fields = ('uuid', 'slug', 'createdAt', 'updatedAt')
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'uuid',
                    'slug',
                    'name',
                    'image',
                    'specs',
                    'description',
                    'price',
                    'stockQuantity',
                    'brand',
                    'category',
                )
            },
        ),
        ('Important dates', {'fields': ('updatedAt', 'createdAt')}),
        (
            'Additional Info',
            {
                'fields': (
                    'sku',
                    'priceCurrency',
                    'isAvailable',
                )
            },
        ),
    )

    @admin.display(description='Бренд')
    def brand_display(self, obj: Product) -> str:
        return format_html(
            '<a href="{}">{}</a>', obj.brand.get_absolute_url(), obj.brand.name
        )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')


@admin.register(CharacteristicGroup)
class CharacteristicGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_display')
    search_fields = ('name',)
    list_filter = ('product',)

    @admin.display(description='Товар')
    def product_display(self, obj: CharacteristicGroup) -> str:
        return format_html(
            '<a href="{}">{}</a>',
            obj.product.get_absolute_url(),
            obj.product.name,
        )


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'group_display')
    search_fields = ('title', 'value')
    list_filter = ('group',)

    @admin.display(description='Группа характеристик')
    def group_display(self, obj: Characteristic) -> str:
        return format_html(
            '<a href="{}">{}</a>', obj.group.get_absolute_url(), obj.group.name
        )


@admin.register(WishlistProduct)
class WishlistProductAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'count', 'total_price', 'user_display')
    search_fields = ('user',)

    @admin.display(description='Пользователь')
    def user_display(self, obj: WishlistProduct) -> str:
        return format_html(
            '<a href="{}">{}</a>',
            obj.user.get_absolute_url(),
            obj.user,
        )
