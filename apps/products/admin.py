from django.contrib import admin
from django.utils.html import format_html

from apps.products.models import Product, CharacteristicGroup, Characteristic


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sku',
        'price',
        'price_currency',
        'stock_quantity',
        'is_available',
        'brand_display',
    )
    list_filter = ('brand', 'price_currency', 'is_available')
    search_fields = ('name', 'sku', 'description')
    readonly_fields = ('uuid',)

    def brand_display(self, obj):
        return format_html(
            '<a href="{}">{}</a>', obj.brand.get_absolute_url(), obj.brand.name
        )

    brand_display.short_description = 'Бренд'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('sku',)
        return self.readonly_fields


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
