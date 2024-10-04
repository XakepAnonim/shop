from django.urls import path

from apps.cart.views import (
    get_cart_handler,
    add_to_cart_handler,
    remove_from_cart_handler,
    delete_from_cart_handler,
    confirm_order_handler,
)

urlpatterns = [
    path('', get_cart_handler),
    path('add/<uuid:product_uuid>/<slug:slug>/', add_to_cart_handler),
    path('remove/<uuid:product_uuid>/<slug:slug>/', remove_from_cart_handler),
    path('delete/<uuid:product_uuid>/<slug:slug>/', delete_from_cart_handler),
    path('<uuid:cart_uuid>/', confirm_order_handler),
]
