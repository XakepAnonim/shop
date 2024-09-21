from django.urls import path

from apps.cart.views import get_cart_handler

urlpatterns = [path('', get_cart_handler)]
