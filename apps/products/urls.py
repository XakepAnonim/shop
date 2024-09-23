from django.urls import path

from apps.products.views import (
    get_product,
    get_wishlist_products,
    post_wishlist_product,
)

urlpatterns = [
    path('<uuid:uuid>/<slug:slug>/', get_product),
    path('wishlist/', get_wishlist_products),
    path('wishlist/<uuid:uuid>/<slug:slug>/', post_wishlist_product),
]
