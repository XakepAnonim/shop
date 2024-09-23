from django.urls import path

from apps.cart.views import get_cart_handler, post_cart_handler

urlpatterns = [
    path('', get_cart_handler),
    path('<uuid:uuid>/<slug:slug>/', post_cart_handler),
]
