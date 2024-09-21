from django.urls import path

from apps.main.views import get_brand_handler, get_brands_handler

urlpatterns = [
    path('brand/<str:name>/', get_brand_handler),
    path('brands', get_brands_handler),
]
