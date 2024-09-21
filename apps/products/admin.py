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

    def brand_display(self, obj):
        return format_html(
            '<a href="{}">{}</a>', obj.brand.get_absolute_url(), obj.brand.name
        )

    brand_display.short_description = 'Бренд'


@admin.register(CharacteristicGroup)
class CharacteristicGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_display')
    search_fields = ('name',)
    list_filter = ('product',)

    def product_display(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            obj.product.get_absolute_url(),
            obj.product.name,
        )

    product_display.short_description = 'Продукт'


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'group_display')
    search_fields = ('title', 'value')
    list_filter = ('group',)

    def group_display(self, obj):
        return format_html(
            '<a href="{}">{}</a>', obj.group.get_absolute_url(), obj.group.name
        )

    group_display.short_description = 'Группа характеристик'


@admin.register(WishlistProduct)
class WishlistProductAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'count', 'total_price', 'user_display')
    search_fields = ('user',)

    def user_display(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            obj.user.get_absolute_url(),
            obj.user,
        )

    user_display.short_description = 'Пользователь'
