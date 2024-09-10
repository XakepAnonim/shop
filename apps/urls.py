from django.urls import path, include

urlpatterns = [
    path('', include('apps.custom_auth.urls')),
    path('users/', include('apps.users.urls')),
]
