from django.urls import path

from apps.products.views import get_product

urlpatterns = [
    path('<uuid:uuid>/<slug:slug>/', get_product)
]
