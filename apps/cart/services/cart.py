from django.db import transaction
from apps.cart.models import Cart, CartItem
from apps.products.models import Product
from apps.users.models import User


class CartService:
    @staticmethod
    def get(user: User) -> Cart:
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    @staticmethod
    @transaction.atomic
    def add_product(user: User, product: Product, quantity: int = 1) -> Cart:
        cart = CartService.get(user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product
        )
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        CartService.update_cart_totals(cart)
        return cart

    @staticmethod
    @transaction.atomic
    def remove_product(
        user: User, product: Product, quantity: int = 1
    ) -> Cart:
        cart = CartService.get(user)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            if cart_item.quantity > quantity:
                cart_item.quantity -= quantity
                cart_item.save()
            else:
                cart_item.delete()
            CartService.update_cart_totals(cart)
        return cart

    @staticmethod
    def update_cart_totals(cart: Cart):
        total = 0
        for item in cart.items.all():
            total += item.product.price * item.quantity
        cart.total_price = total
        cart.save()
