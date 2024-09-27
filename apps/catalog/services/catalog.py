from django.core.cache import cache
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.catalog.models import Category


def get_all_categories() -> QuerySet[Category]:
    """
    Получение полного каталога с предзагрузкой вложенных категорий и продуктов.
    """
    # cache_key = 'all_categories'
    # cached_data = cache.get(cache_key)
    # if cached_data:
    #     return cached_data

    categories = (
        Category.objects.prefetch_related('products')
        .prefetch_related('children')
        .all()
    )
    # # Сохраняем результат в Redis на 10 минут
    # cache.set(cache_key, categories, timeout=600)
    return categories


def get_category(uuid: str, slug: str) -> Category:
    """
    Получение категории по uuid и slug с предзагрузкой
    вложенных категорий и продуктов.
    """
    return get_object_or_404(
        Category.objects.prefetch_related('products', 'children__products'),
        uuid=uuid,
        slug=slug,
    )
