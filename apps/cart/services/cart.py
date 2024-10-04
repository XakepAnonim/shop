import uuid

from django.db import transaction

from apps.cart.models import Cart, CartItem
from apps.products.models import Product
from apps.users.models import User


class CartService:
    """
    Сервис для работы с корзиной
    """

    @staticmethod
    def get(user: User) -> Cart:
        """
        Получение корзины пользователя
        """
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    @staticmethod
    def get_by_uuid(cart_uuid: uuid.uuid4) -> Cart:
        """
        Получение корзины по uuid
        """
        cart = Cart.objects.filter(uuid=cart_uuid).first()
        return cart

    @staticmethod
    def delete(cart: Cart) -> None:
        """
        Удаление корзины
        """
        cart.items.all().delete()
        cart.total_price = 0
        cart.save()

    @classmethod
    @transaction.atomic
    def add_product(cls, user: User, product: Product, quantity: int = 1) -> Cart:
        """
        Добавление товара в корзину
        """
        cart = cls.get(user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product
        )
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        cls.update_cart_totals(cart)
        return cart

    @classmethod
    @transaction.atomic
    def remove_product(cls, user: User, product: Product, quantity: int = 1) -> Cart:
        """
        Удаление товара из корзины
        """
        cart = cls.get(user)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            if cart_item.quantity > quantity:
                cart_item.quantity -= quantity
                cart_item.save()
            else:
                cart_item.delete()
            cls.update_cart_totals(cart)
        return cart

    @staticmethod
    def update_cart_totals(cart: Cart):
        """
        Обновление общего счета корзины
        """
        total = 0
        for item in cart.items.all():
            total += item.product.price * item.quantity
        cart.total_price = total
        cart.save()

    @classmethod
    def delete_product(cls, user: User, product: Product) -> Cart:
        """
        Удаление товара из корзины
        """
        cart = cls.get(user)
        cart_item = CartItem.objects.filter(cart=cart, product=product)
        cart_item.delete()
        return cart
