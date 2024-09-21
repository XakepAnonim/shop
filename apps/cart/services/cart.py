from django.shortcuts import get_object_or_404

from apps.cart.models import Cart
from apps.users.models import User


class CartService:
    @staticmethod
    def get(user: User) -> Cart:
        cart = get_object_or_404(Cart, user=user)
        return cart
