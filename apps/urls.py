from django.urls import path, include

urlpatterns = [
    path('', include('apps.main.urls')),
    path('cart/', include('apps.cart.urls')),
    path('test/', include('apps.test.urls')),
    path('users/', include('apps.users.urls')),
    path('catalog/', include('apps.catalog.urls')),
    path('auth/', include('apps.custom_auth.urls')),
    path('products/', include('apps.products.urls')),
]
