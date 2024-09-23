from django.shortcuts import get_object_or_404

from apps.cart.models import Cart
from apps.products.models import Product
from apps.users.models import User


class CartService:
    @staticmethod
    def get(user: User) -> Cart:
        cart = get_object_or_404(Cart, user=user)
        return cart

    @staticmethod
    def get_or_create(user: User, product: Product) -> Cart:
        """
        Добавление\удаление товара из корзины
        """
        cart, created = Cart.objects.get_or_create(
            user=user,
            defaults={
                'count': 0,
                'total_price': 0,
            },
        )

        if product not in cart.products.all():
            cart.products.add(product)
            cart.count += 1
            cart.total_price += product.price
            cart.save()
        else:
            cart.products.remove(product)
            cart.count -= 1
            cart.total_price -= product.price
            cart.save()

        return cart
