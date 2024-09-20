from django.urls import path

from apps.main.views import get_brand_handler

urlpatterns = [
    path('brand/<str:name>/', get_brand_handler),
]
