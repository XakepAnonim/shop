from django.contrib import admin
from django.utils.html import format_html

from apps.catalog.models import (
    SubCategory,
    MainCategory,
    ProductVariety,
    ProductSubtype,
    ProductType,
)


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 0


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'uuid', 'sub_catergory_display')
    search_fields = ('name',)
    readonly_fields = ('uuid', 'slug')
    inlines = [SubCategoryInline]

    @admin.display(description='Категория')
    def sub_catergory_display(self, obj: MainCategory) -> str:
        links = [
            format_html(
                '<a href="{}">{}</a>',
                sub_category.get_absolute_url(),
                sub_category.name,
            )
            for sub_category in obj.subcategories.all()
        ]
        return format_html(', '.join(links))


class ProductVarietyInline(admin.TabularInline):
    model = ProductVariety
    extra = 0


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'mainCategory',
        'slug',
        'uuid',
        'product_varietys_display',
    )
    search_fields = (
        'name',
        'mainCategory__name',
    )
    readonly_fields = ('uuid', 'slug')
    inlines = [ProductVarietyInline]

    @admin.display(description='Разновидность товара')
    def product_varietys_display(self, obj: SubCategory) -> str:
        links = [
            format_html(
                '<a href="{}">{}</a>',
                product_varietys.get_absolute_url(),
                product_varietys.name,
            )
            for product_varietys in obj.product_varietys.all()
        ]
        return format_html(', '.join(links))


@admin.register(ProductVariety)
class ProductVarietyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'subCategory',
        'slug',
        'uuid',
        'product_types_display',
    )
    search_fields = ('name', 'subCategory__name')
    readonly_fields = ('uuid', 'slug')

    @admin.display(description='Тип товара')
    def product_types_display(self, obj: ProductVariety) -> str:
        links = [
            format_html(
                '<a href="{}">{}</a>',
                product_types.get_absolute_url(),
                product_types.name,
            )
            for product_types in obj.product_types.all()
        ]
        return format_html(', '.join(links))


class ProductSubtypeInline(admin.TabularInline):
    model = ProductSubtype
    extra = 0


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'productVariety',
        'slug',
        'uuid',
        'product_subtypes_display',
    )
    search_fields = ('name', 'productVariety__name')
    readonly_fields = ('uuid', 'slug')
    inlines = [ProductSubtypeInline]

    @admin.display(description='Подтип товара')
    def product_subtypes_display(self, obj: ProductType) -> str:
        links = [
            format_html(
                '<a href="{}">{}</a>',
                product_subtypes.get_absolute_url(),
                product_subtypes.name,
            )
            for product_subtypes in obj.product_subtypes.all()
        ]
        return format_html(', '.join(links))


@admin.register(ProductSubtype)
class ProductSubtypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'productType', 'slug', 'uuid', 'products_display')
    search_fields = ('name', 'productType__name')
    readonly_fields = ('uuid', 'slug')

    @admin.display(description='Товары')
    def products_display(self, obj: ProductSubtype) -> str:
        links = [
            format_html(
                '<a href="{}">{}</a>',
                products.get_absolute_url(),
                products.name,
            )
            for products in obj.products_in_subtype.all()
        ]
        return format_html(', '.join(links))
