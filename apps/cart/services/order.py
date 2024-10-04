from django.db import transaction

from apps.cart.models import Order, Cart
from apps.users.models import User


class OrderService:
    """
    Сервис для работы с заказами
    """

    @staticmethod
    @transaction.atomic
    def create_order(
        cart: Cart,
        delivery_type: str,
        payment_method: str,
        delivery_address: str,
        online_method: None | str,
        delivery_coordinates: None | list[float, float],
        user: User
    ) -> Order:
        """
        Создание заказа
        """
        total_quantity = sum(item.quantity for item in cart.items.all())

        order = Order.objects.create(
            quantity=total_quantity,
            totalPrice=cart.total_price,
            deliveryType=delivery_type,
            paymentMethod=payment_method,
            onlineMethod=online_method,
            deliveryAddress=delivery_address,
            deliveryCoordinates=delivery_coordinates,
            user=user
        )

        for item in cart.items.all():
            order.products.add(item.product)

        return order

    @staticmethod
    @transaction.atomic
    def check_product(cart: Cart) -> None:
        """
        Проверка наличия товара на складе
        """
        try:
            for item in cart.items.all():
                product = item.product
                if product.stockQuantity >= item.quantity:
                    product.stockQuantity -= item.quantity
                    product.save()
                elif product.stockQuantity < item.quantity:
                    raise Exception(f'Не хватает товара {product.name} на складе.')
        except Exception as e:
            raise Exception({'data': {str(e)}})
