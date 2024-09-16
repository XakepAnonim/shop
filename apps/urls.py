from django.urls import path, include

urlpatterns = [
    path('', include('apps.main.urls')),
    path('users/', include('apps.users.urls')),
    path('auth/', include('apps.custom_auth.urls')),
    path('test/', include('apps.test.urls')),
    path('products/', include('apps.products.urls')),
]
