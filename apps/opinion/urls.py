from django.urls import path

from apps.opinion.views import get_product_opinions, add_opinion

urlpatterns = [
    path('', get_product_opinions),
    path('add/', add_opinion),
]
