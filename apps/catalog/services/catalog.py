import uuid

from django.shortcuts import get_object_or_404

from apps.catalog.models import (
    MainCategory,
    SubCategory,
    ProductVariety,
    ProductType,
    ProductSubtype,
)


def get_all_category() -> MainCategory:
    categorys = MainCategory.objects.prefetch_related(
        'subcategories__product_varietys__product_types__product_subtypes__products_in_subtype'
    ).all()
    return categorys


def get_main_category(uuid: uuid.uuid4, slug: str) -> MainCategory:
    catalog = get_object_or_404(
        MainCategory.objects.prefetch_related(
            'subcategories__product_varietys__product_types__product_subtypes__products_in_subtype'
        ),
        uuid=uuid,
        slug=slug,
    )
    return catalog


def get_sub_category(uuid: uuid.uuid4, slug: str) -> SubCategory:
    catalog = get_object_or_404(
        SubCategory.objects.prefetch_related(
            'product_varietys__product_types__product_subtypes__products_in_subtype'
        ),
        uuid=uuid,
        slug=slug,
    )
    return catalog


def get_product_variety(uuid: uuid.uuid4, slug: str) -> ProductVariety:
    catalog = get_object_or_404(
        ProductVariety.objects.prefetch_related(
            'product_types__product_subtypes__products_in_subtype'
        ),
        uuid=uuid,
        slug=slug,
    )
    return catalog


def get_product_type(uuid: uuid.uuid4, slug: str) -> ProductType:
    catalog = get_object_or_404(
        ProductType.objects.prefetch_related(
            'product_subtypes__products_in_subtype'
        ),
        uuid=uuid,
        slug=slug,
    )
    return catalog


def get_product_subtype(uuid: uuid.uuid4, slug: str) -> ProductSubtype:
    catalog = get_object_or_404(
        ProductSubtype.objects.prefetch_related('products_in_subtype'),
        uuid=uuid,
        slug=slug,
    )
    return catalog
