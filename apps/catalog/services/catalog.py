from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.catalog.models import (
    MainCategory,
    SubCategory,
    ProductVariety,
    ProductType,
    ProductSubtype,
)


def get_all_categories() -> QuerySet[MainCategory]:
    """
    Получение каталога
    """
    categories = MainCategory.objects.prefetch_related(
        'subcategories__product_varietys__product_types__product_subtypes__products_in_subtype'
    ).all()
    return categories


def get_main_category(uuid: str, slug: str) -> MainCategory:
    """
    Получение категории по uuid и slug
    """
    main_category = get_object_or_404(
        MainCategory.objects.prefetch_related(
            'subcategories__product_varietys__product_types__product_subtypes__products_in_subtype'
        ),
        uuid=uuid,
        slug=slug,
    )
    return main_category


def get_sub_category(uuid: str, slug: str) -> SubCategory:
    """
    Получение подкатегории по uuid и slug
    """
    sub_category = get_object_or_404(
        SubCategory.objects.prefetch_related(
            'product_varietys__product_types__product_subtypes__products_in_subtype'
        ),
        uuid=uuid,
        slug=slug,
    )
    return sub_category


def get_product_variety(uuid: str, slug: str) -> ProductVariety:
    """
    Получение разновидностей товаров по uuid и slug
    """
    product_variety = get_object_or_404(
        ProductVariety.objects.prefetch_related(
            'product_types__product_subtypes__products_in_subtype'
        ),
        uuid=uuid,
        slug=slug,
    )
    return product_variety


def get_product_type(uuid: str, slug: str) -> ProductType:
    """
    Получение типов товаров по uuid и slug
    """
    product_type = get_object_or_404(
        ProductType.objects.prefetch_related(
            'product_subtypes__products_in_subtype'
        ),
        uuid=uuid,
        slug=slug,
    )
    return product_type


def get_product_subtype(uuid: str, slug: str) -> ProductSubtype:
    """
    Получение подтипов товаров по uuid и slug
    """
    product_subtype = get_object_or_404(
        ProductSubtype.objects.prefetch_related('products_in_subtype'),
        uuid=uuid,
        slug=slug,
    )
    return product_subtype
