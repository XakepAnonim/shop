from django.shortcuts import get_object_or_404

from apps.products.models import WishlistProduct
from apps.users.models import User


class WishlistService:
    @staticmethod
    def get(user: User) -> WishlistProduct:
        wishlist = get_object_or_404(WishlistProduct, user=user)
        return wishlist
