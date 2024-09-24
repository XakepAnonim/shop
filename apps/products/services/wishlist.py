from django.shortcuts import get_object_or_404

from apps.products.models import WishlistProduct, Product
from apps.users.models import User


class WishlistService:
    @staticmethod
    def get(user: User) -> WishlistProduct:
        wishlist = get_object_or_404(WishlistProduct, user=user)
        return wishlist

    @staticmethod
    def get_or_create(user: User, product: Product) -> WishlistProduct:
        """
        Добавление\удаление товара из списка желаемых товаров
        """
        wishlist_product, created = WishlistProduct.objects.get_or_create(
            user=user,
            defaults={
                'count': 0,
                'total_price': 0,
            },
        )

        if product not in wishlist_product.products.all():
            wishlist_product.products.add(product)
            wishlist_product.count += 1
            wishlist_product.total_price += product.price
            wishlist_product.save()
        else:
            wishlist_product.products.remove(product)
            wishlist_product.count -= 1
            wishlist_product.total_price -= product.price
            wishlist_product.save()

        return wishlist_product
