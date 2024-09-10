from django.urls import path

from apps.users.views import manage_user_handler

urlpatterns = [
    path('profile', manage_user_handler),
]
