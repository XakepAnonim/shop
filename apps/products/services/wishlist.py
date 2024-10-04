from django.core.cache import cache
from django.shortcuts import get_object_or_404

from apps.products.models import WishlistProduct, Product
from apps.users.models import User

CACHE_TTL = 60 * 60 * 24  # 1 день


class WishlistService:
    """
    Сервис для работы со списком желаемых товаров
    """

    @staticmethod
    def get(user: User) -> WishlistProduct:
        """
        Получение списка желаемых товаров
        """
        wishlist = get_object_or_404(WishlistProduct, user=user)
        return wishlist

    @staticmethod
    def get_or_create(user: User, product: Product) -> WishlistProduct:
        cache_key = f"wishlist_{user.id}"
        wishlist_product = cache.get(cache_key)

        if wishlist_product is None:
            wishlist_product, created = WishlistProduct.objects.prefetch_related('products').get_or_create(
                user=user,
                defaults={
                    'count': 0,
                    'total_price': 0,
                },
            )
            cache.set(cache_key, wishlist_product, CACHE_TTL)

        products = wishlist_product.products.all()
        if product not in products:
            wishlist_product.products.add(product)
            wishlist_product.count += 1
            wishlist_product.total_price += product.price
            cache.delete(cache_key)
        else:
            wishlist_product.products.remove(product)
            wishlist_product.count -= 1
            wishlist_product.total_price -= product.price
            cache.delete(cache_key)

        wishlist_product.save()
        return wishlist_product
