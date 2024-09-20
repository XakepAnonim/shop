from django.urls import path

from apps.catalog.views import get_catalog_handler, get_category_handler

urlpatterns = [
    path('', get_catalog_handler),
    path('<uuid:uuid>/<slug:slug>/', get_category_handler),
]
