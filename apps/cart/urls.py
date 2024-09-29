from django.urls import path

from apps.cart.views import (
    get_cart_handler,
    add_to_cart_handler,
    remove_from_cart_handler,
    delete_from_cart_handler,
)

urlpatterns = [
    path('', get_cart_handler),
    path('add/<uuid:uuid>/<slug:slug>/', add_to_cart_handler),
    path('remove/<uuid:uuid>/<slug:slug>/', remove_from_cart_handler),
    path('delete/<uuid:uuid>/<slug:slug>/', delete_from_cart_handler),
]
